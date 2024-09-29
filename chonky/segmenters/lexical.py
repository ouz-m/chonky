from typing import List

from chonky.segmenters.base import Segmenter
from chonky.segmenters.models import Segment

import math


class CharacterLevelSegmenter(Segmenter):
	def segment(
		self,
		text: str,
		stride: int,
		overlap: int = 0,
	) -> List[Segment]:
		assert stride > 0, 'Stride must be positive.'
		assert overlap >= 0, 'Overlap must be non-negative.'
		assert stride > overlap, 'Stride must be greater than overlap.'

		text_length = len(text)
		step_length = stride - overlap

		# Calculate number of segments
		n = (text_length - overlap) / step_length
		num_full_segments = max(0, math.floor(n))

		# Create full segments
		segments = [
			Segment(
				content=text[i : i + stride],
				start=i,
				end=min(i + stride, text_length),
			)
			for i in range(0, num_full_segments * step_length, step_length)
		]

		# Add the last segment if there's remaining text
		if n > num_full_segments:
			last_start = num_full_segments * step_length
			segments.append(
				Segment(
					content=text[last_start:],
					start=last_start,
					end=text_length,
				)
			)

		return segments
