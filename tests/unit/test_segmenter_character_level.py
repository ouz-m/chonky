import pytest
from chonky.segmenters.lexical import CharacterLevelSegmenter
from chonky.segmenters.models import Segment


@pytest.fixture
def segmenter():
	return CharacterLevelSegmenter()


def test_basic_segmentation(segmenter):
	text = 'abcdefghij'
	segments = segmenter.segment(text=text, stride=5, overlap=2)
	expected = [
		Segment(content='abcde', start=0, end=5),
		Segment(content='defgh', start=3, end=8),
		Segment(content='ghij', start=6, end=10),
	]
	assert segments == expected


def test_no_overlap(segmenter):
	text = 'abcdefghij'
	segments = segmenter.segment(text=text, stride=5, overlap=0)
	expected = [
		Segment(content='abcde', start=0, end=5),
		Segment(content='fghij', start=5, end=10),
	]
	assert segments == expected


def test_single_character_stride(segmenter):
	text = 'abcde'
	segments = segmenter.segment(text=text, stride=1, overlap=0)
	expected = [
		Segment(content='a', start=0, end=1),
		Segment(content='b', start=1, end=2),
		Segment(content='c', start=2, end=3),
		Segment(content='d', start=3, end=4),
		Segment(content='e', start=4, end=5),
	]
	assert segments == expected


def test_stride_equal_to_text_length(segmenter):
	text = 'abcde'
	segments = segmenter.segment(text=text, stride=5, overlap=0)
	expected = [Segment(content='abcde', start=0, end=5)]
	assert segments == expected


def test_stride_greater_than_text_length(segmenter):
	text = 'abcde'
	segments = segmenter.segment(text=text, stride=10, overlap=0)
	expected = [Segment(content='abcde', start=0, end=5)]
	assert segments == expected


def test_empty_string(segmenter):
	text = ''
	segments = segmenter.segment(text=text, stride=5, overlap=2)
	assert segments == []


def test_invalid_parameters(segmenter):
	text = 'abcde'
	with pytest.raises(AssertionError, match='Stride must be positive.'):
		segmenter.segment(text=text, stride=0, overlap=0)

	with pytest.raises(AssertionError, match='Overlap must be non-negative.'):
		segmenter.segment(text=text, stride=5, overlap=-1)

	with pytest.raises(AssertionError, match='Stride must be greater than overlap.'):
		segmenter.segment(text=text, stride=5, overlap=5)


def test_large_text(segmenter):
	text = 'a' * 1000
	segments = segmenter.segment(text=text, stride=100, overlap=20)
	assert len(segments) == 12
	assert all(len(segment.content) == 100 for segment in segments)
