#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-core/ampel/ingest/CompoundBluePrint.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 01.01.2018
# Last Modified Date: 18.03.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from dataclasses import dataclass, field
from typing import Set, Optional, Dict, List, Union, Tuple, Any
from ampel.type import ChannelId, StrictIterable, DataPointId
from ampel.content.Compound import CompoundElement


@dataclass
class CompoundBluePrint:
	"""
	A specification of the minimal set of :class:`compounds <ampel.content.Compound.Compound>`
	that represent a collection of :class:`datapoints <ampel.content.DataPoint.DataPoint>`,
	as viewed through a set of channels.

	Different channels may select different subsets of the datapoints associated
	with a stock. In addition, some datapoints may be part of a channel's selection, but
	explicitly excluded by a policy, for example one that requires significant
	detections above the noise level.

	This leads to two different identifiers for a subselection:

	strict id:
	  The hash of all the datapoints the subselection contains
	effective id:
	  The hash of only the datapoints that were not marked excluded

	Only one :class:`~ampel.content.Compound.Compound` will be created for each
	*effective* subselection. This allows downstream calculations that operate on equivalent
	subselections to be performed only once. The variants corresponding to each distinct
	strict id may be included as metadata in subclasses of
	:class:`~ampel.content.Compound.Compound`.
	"""

	# save compound lists using effective id as key
	#: Mapping from effective id to compound contents
	d_eid_comp: Dict[bytes, List[Union[DataPointId, CompoundElement]]] = field(default_factory=dict)

	# save channels names using effective id as key
	#: Mapping from effective id to channels
	d_eid_chnames: Dict[bytes, Set[ChannelId]] = field(default_factory=dict)

	# save tuple (chan name, strict id) using effective id as key
	#: Mapping from effective id to (channel, strict id)
	d_eid_tuple_chan_sid: Dict[bytes, Set[Tuple[ChannelId, bytes]]] = field(default_factory=dict)

	# save strict compound difference (wrt to effective compound) using strict if as key
	#: Mapping from strict id to the difference of the strict and effective
	#: compounds, i.e. the set of points excluded from the effective compound
	d_sid_compdiff: Dict[bytes, List[Union[DataPointId, CompoundElement]]] = field(default_factory=dict)

	# save eid <-> compound tags association
	#: Mapping from effective id to compound tags
	d_eid_comptags: Dict[bytes, Set[str]] = field(default_factory=dict)


	def get_effids_for_chans(self, chan_names: StrictIterable[ChannelId]) -> Set[bytes]:
		"""
		:param chan_names: list/tuple/set of channel names
		:returns: a set of effective compound ids representing the union of all
		  channels' views into the underlying datapoints
		"""
		eids = set()
		for chan_name in chan_names:
			for eid in self.d_eid_chnames:
				if chan_name in self.d_eid_chnames[eid]:
					eids.add(eid)
		return eids


	def get_effid_for_chan(self, chan_name: ChannelId) -> Optional[bytes]:
		"""
		:param chan: channel name
		:returns: the effective compound id for the channel, or None if no
		  datapoints were selected for the channel
		"""
		for eid in self.d_eid_chnames:
			if chan_name in self.d_eid_chnames[eid]:
				return eid
		return None


	def get_chans_with_effid(self, eff_comp_id: bytes) -> Set[ChannelId]:
		"""
		:param eff_comp_id: effective compound id
		:returns: the set of channels with the same effective compound id
		"""
		return self.d_eid_chnames[eff_comp_id]


	def get_comp_tags(self, eff_comp_id: bytes) -> Set[str]:
		"""
		:param eff_comp_id: effective compound id
		:returns: tags for the given compound
		"""
		return self.d_eid_comptags[eff_comp_id]


	def get_eff_compound(self, eff_comp_id: bytes) -> List[Union[DataPointId, CompoundElement]]:
		"""
		:param eff_comp_id: effective compound id
		:returns: compound contents
		"""
		return self.d_eid_comp[eff_comp_id]


	def has_flavors(self, compound_id: bytes) -> bool:
		"""
		:returns: True if the effective id corresponds to more than one strict id
		"""

		if compound_id not in self.d_eid_tuple_chan_sid:
			return False

		if len(self.d_eid_tuple_chan_sid[compound_id]) == 0:
			return False

		return True


	def get_compound_flavors(self, compound_id: bytes) -> List[Dict[str, Any]]:
		"""
		:param compound_id: effective compound id
		:returns: the "flavors", or strict ids that correspond to the effective
		  id, and the set of points excluded from each
		"""

		return [
			{'flavor': el[1], 'omitted': self.d_sid_compdiff[el[1]]}
			for el in self.d_eid_tuple_chan_sid[compound_id]
		]


	def get_channel_flavors(self, compound_id: bytes) -> List[Dict[str, Any]]:
		"""
		:param compound_id: effective compound id
		:returns: the "flavors", or strict ids that correspond to the effective
		  id, and channel each was created for
		"""

		return [
			{'channel': el[0], 'flavor': el[1]}
			for el in self.d_eid_tuple_chan_sid[compound_id]
		]
