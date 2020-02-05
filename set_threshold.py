# this function set a list of threshold values in which new
# sensor reading should be within in a safe mode
def value(params: list, sensitivity: float):
	val = [params[0] + sensitivity, params[0] - sensitivity,
				params[1] + sensitivity, params[1] - sensitivity,
				params[2] + sensitivity, params[2] - sensitivity]
	return val