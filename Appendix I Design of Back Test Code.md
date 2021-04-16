## **Appendix I Design of Back Test Code**

The implementation of the back test is based on Python Object-oriented (OOP) programming. OOP can mimic the entities in real life. It can combine the data structures and methods, offering various useful design, such as inheritance, hiding, polymorphism, which is widely adopted in quantitative finance industry. 

The back test program is implemented as a Python Class. This appendix will use simple moving average as an example to explain the code. The implementation of other strategies follow the same logic.

### 1. Instantiation 

**Name:** `__init__()` 

**Purpose:** assign values to necessary attributes or other operations when the object is created. 

**Parameters:** 

- instrument: the input for attribute instrument 
- data: the input for attribute data 

**Design:** we use the historical data to instantiate a python class, so we can run different trading strategy without repeatedly processing the time-series. It also pave the way for the subsequent comparison and plotting methods.

```python
class back_test_bot(object):
    def __init__(self, instrument, data):
        self.instrument = instrument
        self.data = data.dropna()
```



### 2. Attributes

- `instrument`: a `string` meaning the name of the financial instrument

- `data`: a `DataFrame` containing the data of historical financial information

- `range1`: the shorter range day number 

- `range2`: the longer range day number 

- `strategy`: the current trading strategy, 0 for simple moving strategy, 1 for exponential moving strategy, 2 for moving average convergence/divergence

- `sum`: sum of the historical market statistics of the financial instrument and trading strategy 

- `std`: the volatility of the historical volatility of the financial instrument and trading strategy 

  

### 3. Method

#### 3.1 Trading Strategy Application Method

**Name:** `strategy_init_()` 

**Purpose:** create and apply the chosen trading strategy 

**Parameters:** 

- range1: the input for attribute range1
- range2: the input for attribute range2
- strategy: the input for attribute strategy
- smoothing: the smoothing term for exponential moving average, default value 2.

**Design:** 

```python
def strategy_init_(self, range1, range2, strategy, smoothing = 2):
    
    self.range1 = range1
    self.range2 = range2
    self.strategy = strategy
```

Take simple moving average trading strategy as an example, we first assign the input to the attributes of the same name.

```python
if self.strategy == 0:
    # SMA trading strategy
    print("---user choice : moving ave strategy, shorter moving range " + str(range1) + " longer moving range: " + str(range2))
```
If the value of `strategy`is 0, it means the user demands the use of simple moving average strategy. A line of text is printed to signal the start of the strategy implementation.

```python
self.data["range1"] = self.data['Adj Close'].rolling(range1).mean()
self.data["range2"] = self.data['Adj Close'].rolling(range2).mean()
```
Use `rolling()` to select the range of adjusted close, then calculate the moving mean using `mean()`

Store the results in our attribute `data`as a new column named "range1" and "range2"

```python
self.data['Position'] = np.where(self.data['range1'] > self.data['range2'], 1, 0)
print("---portfolio position established ...")
```

Compare the shorter range and longer range moving average

Take long position 1 when the condition is `TRUE`, otherwise take 0. (if allowed, user can also take short position when the condition is `FALSE` by changing the last parameter to negative `float`)

Print message to signal the establishment of the position.

```python
self.data['Returns'] = np.log(self.data['Adj Close'] / self.data['Adj Close'].shift(1))
print("---market Returns calculated ...")
```

Calculate the historical market Returns of the financial instrument and store in a new column named `returns` in our attribute `data` 

Print message to signal the end of calculation process.

```python
self.data['Strategy'] = self.data['Position'].shift(1) * self.data['Returns']
print("---strategy Returns calculate ...")
```

Calculate the historical returns of the trading strategy and store in a new column named `Strategy` in our attribute `data` 

Print message to signal the end of calculation process.

```python
self.data.dropna(inplace=True)
```

Delete the NA data created due to the truncated period for the calculation of the first position.

```python
self.sum = np.exp(self.data[['Returns', 'Strategy']].sum())
self.std = self.data[['Returns', 'Strategy']].std() * 252 ** 0.5
print("---Congrats!!! all result generated, find daily data in results, find stats data in sum and std")
```

Calculate the cumulative sum of the historical returns of the financial instrument and trading strategy and store in attribute `sum` 

Calculate the annual volatility of the financial instrument and trading strategy and store in attribute `std`

Print message to signal the end of trading strategy application process.

### 

#### 3.2 Plot Methods

**Name:** `plot1()` , `plot2()` , `plot3()` , 

**Purpose:** to create a plot of adjusted prices and moving averages.

 Take SMA in `plot2()` method as an example, plot will contain column `Adj Close`, `range1`,and `range2`columns of attribute `data.` 

**Design:** 

```python
    def plot2(self):
        if self.strategy == 0:
            print("---plot1: SMA with positions")
```

Identify the choice of strategy 

Signal the plot method name

```python
        	ax = self.data[["Adj Close", "range1", "range2", "Position"]].plot(secondary_y='Position', figsize=(10, 6))
```
Select the columns of `data`

Set the plot figure size and plot 

```python
        	ax.get_legend().set_bbox_to_anchor((0.25, 0.85))
```

Set the legend design



#### 3.3 Summary Method

**Name:** `summary()` 

**Purpose:** to calculate and print the statistics of the trading strategy

**Parameters:** 

- year: the number of year of our time series data, default value 4

**Design:** 

```python
def summary(self, year = 4):
    if self.strategy == 0:
        print("---- SMA: Sums up the Returns for the strategy and the market")
        print(self.sum/year)
```

Print the annualized sum of returns for the returns for the strategy and the market

```python
    print("---The annualized volatility for the strategy and the market")
    print(self.std)
```
Print the annualized volatility for the strategy and the market