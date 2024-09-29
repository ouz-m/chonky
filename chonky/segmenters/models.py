from typing import Any, Dict, List
from pydantic import BaseModel


class Segment(BaseModel):
	content: str  # String content without leading or trailing whitespace
	start: int
	end: int


class Document(BaseModel):
	segments: List[Segment]
	metadata: Dict[str, Any] = None

	def whole(self) -> str:
		return ' '.join([segment.content for segment in self.segments])

	@property
	def num_segments(self) -> int:
		return len(self.segments)
