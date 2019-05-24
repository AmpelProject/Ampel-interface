#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/base/Observatory.py
# License           : BSD-3-Clause
# Author            : matteo.giomi@desy.de
# Date              : 19.08.2018
# Last Modified Date: 20.08.2018
# Last Modified By  : matteo.giomi@desy.de

import time
import numpy as np
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, AltAz, EarthLocation, get_sun, get_moon

import logging
logging.basicConfig(level = logging.INFO)

def to_time(time):
	if isinstance(time, str):
		return Time(time)
	elif isinstance(Time):
		return time
	else:
		raise TypeError("times can be either `str` or `astropy.time.Time` objects, not %s"
			%type(time))

def get_times(trange, dt_min):
	"""
	Returns an astropy.Time object of time values spaced with resoltion dt 
	in the given time range.
	
	NOTE: trange[1] is not included in the result.
	
	:param iterable trange: list of 2 elements specifying the time range (UTC). 
	Each of them can be either a `str` or `astropy.time.Time`.
	:param float dt_min: resolution for the time grid in minutes.
	:returns: astropy.Time object with the time values. 
	:rtype: astropy.time.Time
	"""
	
	tstart, tend = to_time(trange[0]), to_time(trange[1])
	dt = dt_min*u.min
	nt=int(((tend-tstart).to('min')/dt.to('min')).value)
	return tstart + np.arange(0, nt)*dt


class Observatory():
	"""
	Class to represent an astronomical observatory, providing methods to
	compute visibility of the source at that position.
		
	NOTE:
	all times and computations are rounded to the minute.
		
	Example usage:
	--------------
		
	.. sourcecode:: python
	
		>>> from Observatory import Observatory

		>>> ztf = Observatory('ZTF', 33.3483717, -116.85972959, 1680.)
		INFO:root:computing visibility of source at (ra: 23.462100, dec: 30.659942) from observatory ZTF

		>>> ra, dec = 23.4621, 30.6599417	#M33 coordinates
		>>> ztf.compute_visibility(ra, dec, ('2018-09-19', '2018-09-20'), airmass_th=1.2)
		INFO:root:using visibility constraints:
			-Time resolution: 5.00 min
			-Airmass limit: 1.20
			-Sun altitude: -12.00 deg
			-Moon distance: 30.00 deg
		INFO:root:computed dark times (sun_alt: -12.00) between 2018-09-19 00:00:00.000 and 2018-09-19 23:55:00.000. Total of 9.92 hours of dark
		INFO:root:source is visible for a total of 5.583 hours. Took 7.82e-01 sec.
	"""
	
	version = 0.1
	
	def __init__(self, name, latitude, longitude, altitude=0, logger=None):
		"""
		Init the observatory.
		
		:param str name: name of observatory
		:param float latitude: geographic latitude of observatory, in degrees.
		:param float longitude: geographic longitude of observatory, in degrees.
		longitudes are measured increasing to the east, so west longitudes are negative.
		:param fload altitude: altitude of observatory above reference ellipsoid, in meters.
		"""
		
		self.logger = logger if logger is not None else logging.getLogger()
		
		self.name = name
		self.location = EarthLocation(
								lat=latitude*u.deg,
								lon=longitude*u.deg,
								height=altitude*u.m)
		
		self.has_atmo = False	# use set_atmosphere to set conditions and consider atmospheric refraction
		
		self.logger.info("Initialized Observatory %s at position (lon %.2f deg, lat %.2f deg, alt: %.1f m)"%
			(name, latitude, longitude, altitude))


	def set_atmosphere(self, pressure, temperature, rel_humidity, wlength):
		"""
		set the properties of the atmosphere (and the average wlength of the 
		filter) needed to compute atmospheric refraction at the location of the
		observatory.
			
		:param float pressure: Pascals, atmospheric pressure.
		:param float temperature: degree celsius, temperature
		:param float: relative humidity
		:param float wlength: nanometers, wavelength for wich the refraction is computed. Should be
		close to the average wlength of the filters used.
		"""
		
		self.pressure		= pressure * u.Pa
		self.temperature	= temperature*u.deg_C
		self.rel_humidity	= rel_humidity
		self.av_wlength		= wlength*1e-9*u.m
		
		# some logging
		mssg = "\t\t\t\t\t-pressure: %f Pa\n"%pressure
		mssg+= "\t\t\t\t\t-temperature: %f Celsius\n"%temperature
		mssg+= "\t\t\t\t\t-relatice humidity: %f perc.\n"%rel_humidity
		mssg+= "\t\t\t\t\t-central wavelength: %f nm"%wlength
		self.logger.info("set atmospheric parameters at observatory location: %s"%mssg)
		self.has_atmo = True


	def get_alt_az(self, obstime=None):
		"""
		compute the Altitude-Azimuth coordinate frame for the observatory.
			
		If atmospheric parameters have been set for this observatory (via the set_atmosphere
		method), the visibility will include atmospheric refraction.
			
		:param obstime: (optional)times for which the Alt-Az frame is computed.
		:type obstime: astropy.Time, None
		"""
		obs_altaz=AltAz(location=self.location, obstime=obstime)
		if self.has_atmo:
			self.logger.debug("Including atmospheric refraction.")
			obs_altaz=AltAz(location=self.location, obstime=obstime, 
				pressure=self.pressure, temperature=self.temperature, 
				relative_humidity=self.rel_humidity, obswl=self.av_wlength)
		return obs_altaz


	def compute_sun_moon(self, trange, which='sun', dt_min=5):
		"""
		compute the position of the sun/moon from the location of the observatory
		between the specified time interval.
			
		:param iterable trange: list of 2 elements specifying the time range (UTC). 
		Each of them can be either a `str` or `astropy.time.Time`.
		:param str which: celestial body to 'move'. Either 'sun' or 'moon'
		:param float dt_min: time resolution in minues.
		:returns: position of the sun/moon as observed from this location at the given time.
		:rtype astropy.coordinates.SkyCoord:
		"""
		start = time.time()
		
		# create the time object
		times = get_times(trange, dt_min)
		
		# define the observatory reference frame and move the sun
		obs_altaz = self.get_alt_az()
		if which.lower()=='sun':
			skypos = get_sun(times).transform_to(obs_altaz)
		elif which.lower()=='moon':
			skypos = get_moon(times).transform_to(obs_altaz)
		else:
			raise ValueError("compute_sun_moon accepts either 'sun' or 'moon'. Got %s"%(which))
		end = time.time()
		self.logger.debug("Computing %s motion from %s to %s (res: %.2f min, %d steps). Took %.2f sec"%
			(which, times.min().iso, times.max().iso, dt_min, len(times), (end-start)))
		return skypos


	def get_dark_times(self, trange, dt_min=5, sun_alt_th=-12, return_mask=False):
		"""
		return and array of astropy Time objects for which the sun, at the 
		location of the observatory is below the given altitude threshold.
			
		If atmospheric parameters have been set for this observatory (via the set_atmosphere
		method), the visibility will include atmospheric refraction.
			
		:param itearble trange: list of 2 elements specifying the time range (UTC).
		Each of them can be either a `str` or `astropy.time.Time`.
		:param float dt_min: minutes, time resolution of the computation.
		:param float sun_alt_th: degrees, altitude of the sun defining the twilight.
		:param bool return_mask: weather to return also the binary mask used on the time vector.
		:returns: astropy.Time object with values corresponding to the 'dark time'.
		if return_mask is True, returns (dark_times, mask) where mask is 
		np array of boolean specifiying which positions in the time vector
		are included in dark_times
		:rtype: astropy.time.Time or tuple (depening on return_mask)
		"""
		
		times = get_times(trange, dt_min)
		sun_skypos = self.compute_sun_moon(trange, which='sun', dt_min=dt_min)
		mask = sun_skypos.alt.to('deg').value < sun_alt_th
		dark_times = times[mask]
		self.logger.info("computed dark times (sun_alt: %.2f) between %s and %s. Total of %.2f hours of dark"%
			(sun_alt_th, times.min().iso, times.max().iso, len(dark_times)*dt_min/60.))
		if return_mask:
			return dark_times, mask
		return dark_times


	def compute_airmass(self, zeniths):
		"""
		compute the airmass (elevated observer in a spherical bubble) of the 
		objects whose zenith time series is given.
			
		there are a lot of formulas for this, see e.g:
		https://en.wikipedia.org/wiki/Air_mass_(astronomy)
			
		:param zeniths: set of zenith angles for which the airmass has to be computed. 
		If simple iterable each element must be an angle in radians.
		:type zeniths:  np.array (or array-like) of floats or astropy.coordinates.angles.Angle/
 		:returns: array of airmass values correspondin to the zenith angles.
 		:rtype: array-like
		"""
		
		Re				= 6378136*u.m
		yam, yobs 		= 100*1e3*u.m, self.location.height
		r, y 			= Re/yam, yobs/yam
		cosz			= np.cos(zeniths)
		am = (np.sqrt( ((r + y)*cosz)**2 + 2*r*(1 - y) - y**2 + 1) - (r + y)*cosz )
		self.logger.debug("Computed airmass for %d apparent sky positions"%len(zeniths))
		return am


	def compute_visibility(self, ra, dec, trange, dt_min=5, airmass_th=2, sun_alt_th=-12, min_moon_dist=30):
		"""
		compute visibility of a given sky location from the position of the obseravtory
		and between times tstart and tstop.
			
		If atmospheric parameters have been set for this observatory (via the set_atmosphere
		method), the visibility will include atmospheric refraction.
			
		If moon_dist is given, also the apparent motion of the moon as seen by the
		observatory will be computed and used to make a cut on the distance to the moon.
		NOTE that this will need to download a 10MB file from the internet to get a 
		precise location of the moon (the first time only).
			
		:param float ra: Right Ascension of target location (J2000), degrees
		:param float dec: declination of target location (J2000), degrees
		:param iterable trange: list of 2 elements specifying the time range (UTC).
		Each of them can be either a `str` or `astropy.time.Time`.
		:param float dt_min: minutes, time resolution of the computation.
		:param float airmass_th: maximum airmass.
		:param float sun_alt_th: degrees, altitude of the sun defining the twilight.
		:param min_moon_dist: degrees, minimum distance of object from the Moon. If None, 
		saves up time not computing the position of the Moon
		:type min_moon_dist: float or None
		:returns: time values for which the conditions on which the visibility are satisfied.
		:rtype: astropy.time.Time
		"""
		start = time.time()
		
		# create the sky coordinate object for the target
		target_skypos = SkyCoord(ra=ra*u.deg, dec=dec*u.deg)
		self.logger.info("computing visibility of source at (ra: %f, dec: %f) from observatory %s"%
			(ra, dec, self.name))
		mssg = "\t\t\t\t\t-Time resolution: %.2f min\n"%dt_min
		mssg+= "\t\t\t\t\t-Airmass limit: %.2f\n"%airmass_th
		mssg+= "\t\t\t\t\t-Sun altitude: %.2f deg"%sun_alt_th
		if not min_moon_dist is None:
			mssg+= "\n\t\t\t\t\t-Moon distance: %.2f deg"%min_moon_dist
		self.logger.info("using visibility constraints:\n%s"%mssg)
		
		# find out the array of dark times
		dark_times, dark_mask = self.get_dark_times(
			trange, dt_min=dt_min, sun_alt_th=sun_alt_th, return_mask=True)
		
		# define the alt-az frame of the observatory
		obs_altaz = self.get_alt_az(obstime = dark_times)
		
		# target position in the alt-az frame of the observatory and its airmass
		target_pos = target_skypos.transform_to(obs_altaz)
		am_values = self.compute_airmass(target_pos.zen)
		
		# and build up the final visibility mask (the sun is already included)
		# eventually compute the moon and cut on the distance to the moon
		is_visible  = am_values < airmass_th
		if not min_moon_dist is None:
			moon_pos = self.compute_sun_moon(trange, which='moon', dt_min=dt_min)
			moon_pos = moon_pos[dark_mask]
			moon_dist = target_pos.separation(moon_pos)
			is_visible = np.logical_and(is_visible, moon_dist > min_moon_dist*u.deg)

		# done, print some stats and return
		times_when_visible = dark_times[is_visible]
		tot_vis_time = len(times_when_visible)*dt_min
		end = time.time()
		self.logger.info("source is visible for a total of %.3f hours. Took %.2e sec"%
			(tot_vis_time/60., (end-start)))
		return times_when_visible

