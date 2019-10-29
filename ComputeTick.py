import pandas as pdfrom pandas.tseries.offsets import BDayimport numpy as npimport osclass ComputeTick:	def __init__(self, target_month, start_date, end_date):		self._start_date = start_date		self._end_date = end_date		self._target_month = pd.Series(pd.to_datetime(target_month)).dt.to_period('m')		self._fn = []		self.monthly_len = None		self.monthly_min = None		self.monthly_max = None		self._bin = None		self._intervals = None		self.precision = None		self.monthly_median = None		self.monthly_mean = None			def getFileName(self):		date_range = pd.date_range(start=self._start_date, end=self._end_date, freq=BDay())		for i in range(int(np.ceil(len(date_range)/5))-1):			if i != int(np.ceil(len(date_range)/5))-2:				startd = date_range[(0+i*5)]				endd = date_range[(0+(i+1)*5)]			else:				startd = date_range[(0+i*5)]				endd = date_range[len(date_range)-1]			if pd.Series(startd).dt.to_period('m')[0] == self._target_month[0]:				file_name = os.getcwd() + "/TickDataNGc1" + "_" + str(startd.date()) + "_" + str(endd.date()) + ".json"				self._fn.append(file_name)	@staticmethod	def loadTRtickdatalite(fn):		df = pd.read_json(fn)		df.sort_index(inplace=True)		df['t'] = pd.to_datetime(df.Date_Time)		df.set_index('t', drop=True, inplace=True)		df = df.tz_localize(None)		return df	def computeMaxMinLen(self):		max_list = []		min_list = []		mean_list = []		len_list = []		for fn in self._fn:			df = self.loadTRtickdatalite(fn)			df = df.iloc[np.where(pd.Series(pd.to_datetime(df.index)).dt.to_period('m') == self._target_month[0])]			max_list.append(df.Price.max())			min_list.append(df.Price.min())			mean_list.append(df.Price.mean())			len_list.append(len(df.Price))			del df				self.monthly_min = min(min_list)		self.monthly_max = max(max_list)		self.monthly_len = sum(len_list)		self.monthly_mean = np.multiply(len_list, mean_list)/self.monthly_len			def setUpBin(self, N):		self._intervals = np.linspace(self.monthly_min, self.monthly_max, num=N+1)		self._bin = {i: 0 for i in range(len(self._intervals)-1)}		self.precision = (self.monthly_max - self.monthly_min)/N	def FillBinwithCount(self):		for fn in self._fn:			df = self.loadTRtickdatalite(fn)			df = df.iloc[np.where(pd.Series(pd.to_datetime(df.index)).dt.to_period('m') == self._target_month[0])]			for val in df.Price:				for i in range(len(self._intervals)-1):					if self._intervals[i] <= val <= self._intervals[i+1]:						self._bin[i] += 1						break		def FindMedian(self):		if self.monthly_len % 2 != 0:			target = (self.monthly_len+1)/2			cum_len = 0			for i in range(len(self._intervals)-1):				if cum_len < target:					cum_len += self._bin[i]				else:					break			self.monthly_median = self._intervals[i-1] + self.precision/2		else:			target = self.monthly_len/2			cum_len = 0			for i in range(len(self._intervals)-1):				if cum_len < target:					cum_len += self._bin[i]				else:					break			if cum_len == target:				self.monthly_median = self._intervals[i]			else:				self.monthly_median = self._intervals[i-1] + self.precision/2