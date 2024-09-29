from abc import ABC, abstractmethod
from typing import List

from chonky.segmenters.models import Segment


class Segmenter(ABC):
	@abstractmethod
	def segment(self, **kwargs) -> List[Segment]:
		pass
