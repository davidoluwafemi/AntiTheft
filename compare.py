# this function determines whether or not the
# new accelerator sensor value is within the range
# of the threshold value
def trigger_bool(val: list, var: list):
	if var[0] > val[0] or var[0] < val[1] or var[1] \
		> val[2] or var[1] < val[3] or var[2] > \
		val[4] or var[2] < val[5]:
		return True
	else:
		return False