import pytest


def time_format(duration):
	'''
	YT uses ISO 8601 to format time and return it as a string as PT1H4M3S (PT is Time Duration, H is Hour, M is Minute and S is Second)
	This function dissects the string and separates hours, minutes and seconds for a more convenient view
	'''
	try:
		duration = duration[2:]
		#print(duration)
		h, m, s = duration.find("H"), duration.find("M"), duration.find("S")
		seconds = duration[m+1:s]
		if h > 0:
			minutes = duration[h+1:m]
			hours = duration[:h]
			return hours + " hours " + minutes + " minutes " + seconds + " seconds"
		else:
			minutes = duration[:m]
			return minutes + " minutes " + seconds + " seconds"

	except Exception as e:
		print(f"Time/Hour format error: {e}")


def test_time_format():
	assert time_format("PT1H4M3S") == "1 hours 4 minutes 3 seconds"