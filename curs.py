import sys
import datetime
import requests

def check arguments(argv):
	if len(argv)==1:
		date1 = datetime.date(year=datetime.datetime.now().date().year, month=datetime.datetime.now().date().month, day=1)
		date2 = today


	try:
		if len(argv)>1:
			if argv[1]=="today":
				print "Today's currency: %s" % get_currency(today)
				return
			date1 = datetime.datetime.strptime(argv[1], "%Y-%m-%d").date()
			if len(argv)>2:
				date2 = datetime.datetime.strptime(argv[2], "%Y-%m-%d").date()
			else:
				date2 = today
		if not date1 or not date2:
			print "Incorrect dates!"
			print "Usage: python curs.py 2013-12-01 2013-12-20"
			return None, None
	except Exception:
		print "Exception while processing the parameters %s" % argv
		return None, None

	return date1, date2

def get_currency(date):
	return float(requests.get('http://www.infovalutar.ro/bnr/%d/%d/%d/EUR' % (date.year, date.month, date.day)).text)


def get_currency():
	# compute the medium value of each day's currency between the specified dates
	date1 = date2 = None
	today = datetime.datetime.now().date()

	date1, date2 = check arguments(sys.argv)

	if not date1 or not date2:
		return

	# order the dates
	difference = date2-date1
	if difference.days<0:
		tmp = date1
		date1 = date2
		date2 = tmp
		difference = date1-date2

	#print "Computing the currency between %s and %s (%s days)" % (date1, date2, difference.days)

	currency = []
	for day in range(difference.days+1):
		# www.infovalutar.ro/bnr/2013/11/27/EUR
		# print 'www.infovalutar.ro/bnr/%d/%d/%d/EUR' % (date.year, date.month, date.day)
		date = date1+datetime.timedelta(days=day)
		# add only weekdays
		if date.isoweekday() in range(1, 6):
			currency.append(get_currency(date))

	print "Computing the currency between %s and %s (%s working days/%s total days)" % (date1, date2, len(currency), difference.days)

	median_currency = sum(currency)/len(currency)
	if len(currency) < 50:
		print currency

	print "Median currency: %s" % median_currency


if __name__ == "__main__":
	get_currency()
