# import os
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.agents import AgentExecutor, create_react_agent
# from langchain import hub
# from langchain.memory import ConversationBufferMemory

# operator_reference = """
# You are in a quant research environment.
# You can use only Regular or base type of operators
# Arithmetic
# abs(x)
# base
# Combo, Regular, Selection
# Absolute value of x
# add(x, y, filter = false), x + y
# base
# Combo, Regular, Selection
# Add all inputs (at least 2 inputs required). If filter = true, filter all input NaN to 0 before adding
# arc_sin(x)
# genius
# Combo, Regular, Selection
# If -1 <= x <= 1: arcsin(x); else NaN
# densify(x)
# base
# Combo, Regular
# Converts a grouping field of many buckets into lesser number of only available buckets so as to make working with grouping fields computationally efficient
# Show more
# divide(x, y), x / y
# base
# Combo, Regular, Selection
# x / y
# exp(x)
# genius
# Combo, Regular, Selection
# Natural exponential function: e^x
# fraction(x)
# genius
# Combo, Regular, Selection
# This operator removes the whole number part and returns the remaining fraction part with sign
# Show more
# inverse(x)
# base
# Combo, Regular, Selection
# 1 / x
# log(x)
# base
# Combo, Regular, Selection
# Natural logarithm. For example: Log(high/low) uses natural logarithm of high/low ratio as stock weights.
# log_diff(x)
# genius
# Combo, Regular
# Returns log(current value of input or x[t] ) - log(previous value of input or x[t-1])
# Show more
# max(x, y, ..)
# base
# Combo, Regular, Selection
# Maximum value of all inputs. At least 2 inputs are required
# Show more
# min(x, y ..)
# base
# Combo, Regular, Selection
# Minimum value of all inputs. At least 2 inputs are required
# Show more
# multiply(x ,y, ... , filter=false), x * y
# base
# Combo, Regular, Selection
# Multiply all inputs. At least 2 inputs are required. Filter sets the NaN values to 1
# Show more
# nan_mask(x, y)
# genius
# Combo, Regular
# replace input with NAN if input's corresponding mask value or the second input here, is negative
# Show more
# pasteurize(x)
# genius
# Combo, Regular
# Set to NaN if x is INF or if the underlying instrument is not in the Alpha universe. This operator may help reduce outliers.
# power(x, y)
# base
# Combo, Regular, Selection
# x ^ y
# Show more
# reverse(x)
# base
# Combo, Regular, Selection
#  - x
# s_log_1p(x)
# genius
# Combo, Regular, Selection
# Confine function to a shorter range using logarithm such that higher input remains higher and negative input remains negative as an output of resulting function and -1 or 1 is an asymptotic value
# Show more
# sigmoid(x)
# genius
# Combo, Regular, Selection
# Returns 1 / (1 + exp(-x))
# sign(x)
# base
# Combo, Regular, Selection
# if input > 0, return 1; if input < 0, return -1; if input = 0, return 0; if input = NaN, return NaN;
# signed_power(x, y)
# base
# Combo, Regular, Selection
# x raised to the power of y such that final result preserves sign of x
# Show more
# sqrt(x)
# base
# Combo, Regular, Selection
# Square root of x
# subtract(x, y, filter=false), x - y
# base
# Combo, Regular, Selection
# x-y. If filter = true, filter all input NaN to 0 before subtracting
# tanh(x)
# genius
# Combo, Regular, Selection
# Hyperbolic tangent of x
# Show more
# to_nan(x, value=0, reverse=false)
# genius
# Combo, Regular, Selection
# Convert value to NaN or NaN to value if reverse=true
# Logical
# and(input1, input2)
# base
# Combo, Regular, Selection
# Logical AND operator, returns true if both operands are true and returns false otherwise
# if_else(input1, input2, input 3)
# base
# Combo, Regular, Selection
# If input1 is true then return input2 else return input3.
# Show more
# input1 < input2
# base
# Combo, Regular, Selection
# If input1 < input2 return true, else return false
# input1 <= input2
# base
# Combo, Regular, Selection
# Returns true if input1 <= input2, return false otherwise
# input1 == input2
# base
# Combo, Regular, Selection
# Returns true if both inputs are same and returns false otherwise
# input1 > input2
# base
# Combo, Regular, Selection
# Logic comparison operators to compares two inputs
# input1 >= input2
# base
# Combo, Regular, Selection
# Returns true if input1 >= input2, return false otherwise
# input1!= input2
# base
# Combo, Regular, Selection
# Returns true if both inputs are NOT the same and returns false otherwise
# is_nan(input)
# base
# Combo, Regular, Selection
# If (input == NaN) return 1 else return 0
# Show more
# not(x)
# base
# Combo, Regular, Selection
# Returns the logical negation of x. If x is true (1), it returns false (0), and if input is false (0), it returns true (1).
# or(input1, input2)
# base
# Combo, Regular, Selection
# Logical OR operator returns true if either or both inputs are true and returns false otherwise
# Time Series
# days_from_last_change(x)
# base
# Combo, Regular
# Amount of days since last change of x
# hump(x, hump = 0.01)
# base
# Combo, Regular
# Limits amount and magnitude of changes in input (thus reducing turnover)
# Show more
# hump_decay(x, p=0)
# genius
# Combo, Regular
# This operator helps to ignore the values that changed too little corresponding to previous ones
# Show more
# inst_tvr(x, d)
# genius
# Combo, Regular
# Total trading value / Total holding value in the past d days
# jump_decay(x, d, sensitivity=0.5, force=0.1)
# genius
# Combo, Regular
# If there is a huge jump in current data compare to previous one
# Show more
# kth_element(x, d, k)
# base
# Combo, Regular
# Returns K-th value of input by looking through lookback days. This operator can be used to backfill missing data if k=1
# Show more
# last_diff_value(x, d)
# base
# Combo, Regular
# Returns last x value not equal to current x value from last d days
# ts_arg_max(x, d)
# base
# Combo, Regular
# Returns the relative index of the max value in the time series for the past d days. If the current day has the max value for the past d days, it returns 0. If previous day has the max value for the past d days, it returns 1
# Show more
# ts_arg_min(x, d)
# base
# Combo, Regular
# Returns the relative index of the min value in the time series for the past d days; If the current day has the min value for the past d days, it returns 0; If previous day has the min value for the past d days, it returns 1.
# Show more
# ts_av_diff(x, d)
# base
# Combo, Regular
# Returns x - tsmean(x, d), but deals with NaNs carefully. That is NaNs are ignored during mean computation
# Show more
# ts_backfill(x,lookback = d, k=1, ignore="NAN")
# base
# Combo, Regular
# Backfill is the process of replacing the NAN or 0 values by a meaningful value (i.e., a first non-NaN value)
# Show more
# ts_co_kurtosis(y, x, d)
# genius
# Combo, Regular
# Returns cokurtosis of y and x for the past d days
# Show more
# ts_co_skewness(y, x, d)
# genius
# Combo, Regular
# Returns coskewness of y and x for the past d days
# Show more
# ts_corr(x, y, d)
# base
# Combo, Regular
# Returns correlation of x and y for the past d days
# Show more
# ts_count_nans(x ,d)
# base
# Combo, Regular
# Returns the number of NaN values in x for the past d days
# ts_covariance(y, x, d)
# base
# Combo, Regular
# Returns covariance of y and x for the past d days
# ts_decay_exp_window(x, d, factor = f)
# genius
# Combo, Regular
# Returns exponential decay of x with smoothing factor for the past d days
# Show more
# ts_decay_linear(x, d, dense = false)
# base
# Combo, Regular
# Returns the linear decay on x for the past d days. Dense parameter=false means operator works in sparse mode and we treat NaN as 0. In dense mode we do not.
# Show more
# ts_delay(x, d)
# base
# Combo, Regular
# Returns x value d days ago
# ts_delta(x, d)
# base
# Combo, Regular
# Returns x - ts_delay(x, d)
# ts_delta_limit(x, y, limit_volume=0.1)
# genius
# Combo, Regular
# Limit the change in the Alpha position x between dates to a specified fraction of y. The "limit_volume" can be in the range of 0 to 1. Also, please be aware of the scaling for x and y. Besides setting y as adv20 or volume related data, you can also set y as a constant.
# ts_entropy(x,d)
# genius
# Combo, Regular
# For each instrument, we collect values of input in the past d days and calculate the probability distribution then the information entropy via a histogram as a result
# Show more
# ts_ir(x, d)
# genius
# Combo, Regular
# Return information ratio ts_mean(x, d) / ts_std_dev(x, d)
# ts_kurtosis(x, d)
# genius
# Combo, Regular
# Returns kurtosis of x for the last d days
# Show more
# ts_max(x, d)
# genius
# Combo, Regular
# Returns max value of x for the past d days
# ts_max_diff(x, d)
# genius
# Combo, Regular
# Returns x - ts_max(x, d)
# ts_mean(x, d)
# base
# Combo, Regular
# Returns average value of x for the past d days.
# ts_median(x, d)
# genius
# Combo, Regular
# Returns median value of x for the past d days
# ts_min(x, d)
# genius
# Combo, Regular
# Returns min value of x for the past d days
# ts_min_diff(x, d)
# genius
# Combo, Regular
# Returns x - ts_min(x, d)
# ts_min_max_cps(x, d, f = 2)
# genius
# Combo, Regular
# Returns (ts_min(x, d) + ts_max(x, d)) - f * x. If not specified, by default f = 2
# ts_min_max_diff(x, d, f = 0.5)
# genius
# Combo, Regular
# Returns x - f * (ts_min(x, d) + ts_max(x, d)). If not specified, by default f = 0.5
# ts_percentage(x, d, percentage=0.5)
# genius
# Combo, Regular
# Returns percentile value of x for the past d days
# Show more
# ts_product(x, d)
# base
# Combo, Regular
# Returns product of x for the past d days
# Show more
# ts_quantile(x,d, driver="gaussian" )
# base
# Combo, Regular
# It calculates ts_rank and apply to its value an inverse cumulative density function from driver distribution. Possible values of driver (optional ) are "gaussian", "uniform", "cauchy" distribution where "gaussian" is the default.
# ts_rank(x, d, constant = 0)
# base
# Combo, Regular
# Rank the values of x for each instrument over the past d days, then return the rank of the current value + constant. If not specified, by default, constant = 0.
# ts_regression(y, x, d, lag = 0, rettype = 0)
# base
# Combo, Regular
# Returns various parameters related to regression function
# Show more
# ts_returns (x, d, mode = 1)
# genius
# Combo, Regular
# Returns the relative change in the x value
# Show more
# ts_scale(x, d, constant = 0)
# base
# Combo, Regular
# Returns (x - ts_min(x, d)) / (ts_max(x, d) - ts_min(x, d)) + constant. This operator is similar to scale down operator but acts in time series space
# Show more
# ts_skewness(x, d)
# genius
# Combo, Regular
# Return skewness of x for the past d days
# Show more
# ts_std_dev(x, d)
# base
# Combo, Regular
# Returns standard deviation of x for the past d days
# ts_step(1)
# base
# Combo, Regular
# Returns days' counter
# ts_sum(x, d)
# base
# Combo, Regular
# Sum values of x for the past d days.
# ts_target_tvr_decay(x, lambda_min=0, lambda_max=1, target_tvr=0.1)
# genius
# Combo, Regular
# Tune "ts_decay" to have a turnover equal to a certain target, with optimization weight range between lambda_min, lambda_max
# ts_target_tvr_delta_limit(x, y, lambda_min=0, lambda_max=1, target_tvr=0.1)
# genius
# Combo, Regular
# Tune "ts_delta_limit" to have a turnover equal to a certain target with optimization weight range between lambda_min, lambda_max. Also, please be aware of the scaling for x and y. Besides setting y as adv20 or volume related data, you can also set y as a constant.
# ts_target_tvr_hump(x, lambda_min=0, lambda_max=1, target_tvr=0.1)
# genius
# Combo, Regular
# Tune "hump" to have a turnover equal to a certain target with optimization weight range between lambda_min, lambda_max.
# ts_vector_neut(x,y,d)
# genius
# Combo, Regular
# Returns x- ts_vector_proj(x,y,d)
# ts_zscore(x, d)
# base
# Combo, Regular
# Z-score is a numerical measurement that describes a value's relationship to the mean of a group of values. Z-score is measured in terms of standard deviations from the mean: (x - tsmean(x,d)) / tsstddev(x,d). This operator may help reduce outliers and drawdown.
# Cross Sectional
# generalized_rank(open, m=1)
# genius
# Combo, Regular
# The idea is that difference between instrument values raised to the power of m is added to the rank of instrument with bigger value and subtracted from the rank of instrument with lesser value. More details in the notes at the end of page
# Show more
# multi_regression(y, x1, x2,..., days=0, lag=0, solver="SVD")
# genius
# Combo, Regular
# Perform multivariable regression of multiple independent variables (x1,x2,...) on a dependent variable (y) across number of days. If days = n (n >= 0), will include past n days in the regression. Setting days = 0 indicates that we're only using today (x1, x2, ...) to predict y. If lag = m (m >= 0), will lag (x1, x2, ...) for m days for prediction. Options for solver: "SVD"(default), "QR", "NORMAL"
# normalize(x, useStd = false, limit = 0.0)
# base
# Combo, Regular
# Calculates the mean value of all valid alpha values for a certain date, then subtracts that mean from each element
# Show more
# quantile(x, driver = gaussian, sigma = 1.0)
# base
# Combo, Regular
# Rank the raw vector, shift the ranked Alpha vector, apply distribution (gaussian, cauchy, uniform). If driver is uniform, it simply subtract each Alpha value with the mean of all Alpha values in the Alpha vector
# Show more
# rank(x, rate=2)
# base
# Combo, Regular
# Ranks the input among all the instruments and returns an equally distributed number between 0.0 and 1.0. For precise sort, use the rate as 0
# Show more
# regression_neut(y, x)
# genius
# Combo, Regular
# Conducts the cross-sectional regression on the stocks with Y as target and X as the independent variable
# Show more
# regression_proj(y, x)
# genius
# Combo, Regular
# Conducts the cross-sectional regression on the stocks with Y as target and X as the independent variable
# Show more
# scale(x, scale=1, longscale=1, shortscale=1)
# base
# Combo, Regular
# Scales input to booksize. We can also scale the long positions and short positions to separate scales by mentioning additional parameters to the operator
# Show more
# scale_down(x,constant=0)
# genius
# Combo, Regular
# Scales all values in each day proportionately between 0 and 1 such that minimum value maps to 0 and maximum value maps to 1. Constant is the offset by which final result is subtracted
# Show more
# truncate(x,maxPercent=0.01)
# genius
# Combo, Regular
# Operator truncates all values of x to maxPercent. Here, maxPercent is in decimal notation
# Show more
# vector_neut(x, y)
# genius
# Combo, Regular
# For given vectors x and y, it finds a new vector x* (output) such that x* is orthogonal to y
# Show more
# vector_proj(x, y)
# genius
# Combo, Regular
# Returns vector projection of x onto y.
# winsorize(x, std=4)
# base
# Combo, Regular
# Winsorizes x to make sure that all values in x are between the lower and upper limits, which are specified as multiple of std.
# zscore(x)
# base
# Combo, Regular
# Z-score is a numerical measurement that describes a value's relationship to the mean of a group of values. Z-score is measured in terms of standard deviations from the mean
# Show more
# Vector
# vec_avg(x)
# base
# Combo, Regular
# Taking mean of the vector field x
# vec_count(x)
# genius
# Combo, Regular
# Number of elements in vector field x
# vec_filter(vec, value=nan)
# genius
# Combo, Regular
# Filter vector by values, such as nan. Can filter many values at once, for example: vec_filter(vec, value="nan 0 10"). Please note the output of this VECTOR will still be vector data.
# vec_ir(x)
# genius
# Combo, Regular
# Information Ratio (Mean / Standard Deviation) of vector field x
# vec_max(x)
# genius
# Combo, Regular
# Maximum value form vector field x
# vec_min(x)
# genius
# Combo, Regular
# Minimum value form vector field x
# vec_norm(x)
# genius
# Combo, Regular
# Sum of all absolute values of vector field x
# vec_powersum(x,constant=2)
# genius
# Combo, Regular
# Sum of power of vector field x
# vec_sum(x)
# base
# Combo, Regular
# Sum of vector field x
# Transformational
# bucket(rank(x), range="0, 1, 0.1" or buckets = "2,5,6,7,10")
# base
# Combo, Regular
# Convert float values into indexes for user-specified buckets. Bucket is useful for creating group values, which can be passed to GROUP as input
# Show more
# generate_stats(alpha)
# base
# Combo
# The generate_stats() operator calculates Alpha statistics for each day in the IS period. It takes an input of selected Alphas with shape = (A x D x I). It outputs daily statistics for each Alpha with shape = (S x D x A), where S is the number of statistics calculated.
# left_tail(x, maximum = 0)
# genius
# Combo, Regular
# NaN everything greater than maximum, maximum should be constant
# Show more
# right_tail(x, minimum = 0)
# genius
# Combo, Regular
# NaN everything less than minimum, minimum should be constant
# Show more
# tail(x, lower = 0, upper = 0, newval = 0)
# genius
# Combo, Regular
# If (x > lower AND x < upper) return newval, else return x. Lower, upper, newval should be constants
# Show more
# trade_when(x, y, z)
# base
# Combo, Regular
# Used in order to change Alpha values only under a specified condition and to hold Alpha values in other cases. It also allows to close Alpha positions (assign NaN values) under a specified condition
# Show more
# Group
# combo_a(alpha, nlength = 250, mode = 'algo1')
# base
# Combo
# Combines multiple alpha signals into a single weighted output by balancing each alpha's historical return with its variability over the most recent nlength days. The parameter mode selects one of the several weighted approaches (algo1, algo2, algo3), each of which handles the tradeoff between performance and stability differently.
# group_backfill(x, group, d, std = 4.0)
# base
# Combo, Regular
# If a certain value for a certain date and instrument is NaN, from the set of same group instruments, calculate winsorized mean of all non-NaN values over last d days
# Show more
# group_cartesian_product(g1, g2)
# genius
# Combo, Regular
# Merge two groups into one group. If originally there are len_1 and len_2 group indices in g1 and g2, there will be len_1 * len_2 indices in the new group.
# group_count(x, group)
# genius
# Combo, Regular
# Gives the number of instruments in the same group (e.g. sector) which have valid values of x. For example, x=1 gives the number of instruments in each group (without regard for whether any particular field has valid data). This operator improves weight coverage and may help to reduce drawdown risk.
# group_extra(x, weight, group)
# genius
# Combo, Regular
# Replaces NaN values by their corresponding group means.
# group_max(x, group)
# genius
# Combo, Regular
# Maximum of x for all instruments in the same group.
# group_mean(x, weight, group)
# base
# Combo, Regular
# All elements in group equals to the mean
# Show more
# group_median(x, group)
# genius
# Combo, Regular
# All elements in group equals to the median value of the group.
# group_min(x, group)
# genius
# Combo, Regular
# All elements in group equals to the min value of the group.
# group_multi_regression(y, x1, x2, ..., group, days=0, lag=0, solver="SVD")
# genius
# Combo, Regular
# Perform multivariable regression for each data points in a group. For more information, please refer to multi_regression. Options for solver: "SVD"(default), "QR", "NORMAL"
# group_neutralize(x, group)
# base
# Combo, Regular
# Neutralizes Alpha against groups. These groups can be subindustry, industry, sector, country or a constant
# Show more
# group_normalize(x, group, constantCheck=False, tolerance=0.01, scale=1)
# genius
# Combo, Regular
# Normalizes input such that each group's absolute sum is 1
# group_percentage(x, group, percentage=0.5)
# genius
# Combo, Regular
# All elements in group equals to the value over the percentage of the group. Percentage = 0.5 means value is equal to group_median(x, group)
# group_rank(x, group)
# base
# Combo, Regular
# Each elements in a group is assigned the corresponding rank in this group
# Show more
# group_scale(x, group)
# base
# Combo, Regular
# Normalizes the values in a group to be between 0 and 1. (x - groupmin) / (groupmax - groupmin)
# group_std_dev(x, group)
# genius
# Combo, Regular
# All elements in group equals to the standard deviation of the group.
# group_sum(x, group)
# genius
# Combo, Regular
# Sum of x for all instruments in the same group.
# group_vector_neut(x,y,g)
# genius
# Combo, Regular
# Similar to vector_neut(x, y) but x neutralize to y for each group g which can be any classifier such as subindustry, industry, sector, etc.
# group_zscore(x, group)
# base
# Combo, Regular
# Calculates group Z-score - numerical measurement that describes a value's relationship to the mean of a group of values. Z-score is measured in terms of standard deviations from the mean. zscore = (data - mean) / stddev of x for each instrument within its group.
# Special
# in
# base
# Selection
# in
# inst_pnl(x)
# genius
# Combo, Regular
# Generate pnl per instruments. Please note that the use of the inst_pnl() operator in an Alpha Expression is considered as utilizing the pv1 dataset (Price Volume Data for Equity) since it relies on pv1 data for calculations.
# self_corr(input)
# base
# Combo
# Taking an input matrix of (D x N) with lookback="K", producing an output matrix of (D x N x N), where each output(di, j, k) refers to correlation of input(di-K:di, j) and input(di-K:di, k). Outputs (D x N x N) from the input of (D x N)
# universe_size
# base
# Selection
# universe_size
# Reduce
# reduce_avg(input, threshold=0)
# base
# Combo
# Average of non-NAN elements of d(..., :). Threshold: Minimum required number of valid (non-nan) values. If there is not enough valid values, then the output is nan. 0 means no limit.threshold (Default: 0) *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)).
# reduce_choose(input, nth, ignoreNan=true)
# base
# Combo
# Choose the 'nth' element in the array, return NAN if not found. Threshold: nth="" (Required) ignoreNan="true|false" (Default: true) *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)).
# reduce_count(input, threshold)
# base
# Combo
# Count the number of element of d(..., :) > threshold. threshold= *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)).
# reduce_ir(input)
# base
# Combo
# IR of values in the array *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)).
# reduce_kurtosis(input)
# base
# Combo
# Kurtosis of values in the array ***Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. If input matrix is (D x N), output matrix (D x 1) If input matrix is (D x N X N), output matrix (D x N X 1) The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)).
# reduce_max(input)
# base
# Combo
# Maximum of elements of d(..., :) *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)).
# reduce_min(input)
# base
# Combo
# Minimum of elements of d(..., :) ***Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. If input matrix is (D x N), output matrix (D x 1) If input matrix is (D x N X N), output matrix (D x N X 1) The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)).
# reduce_norm(input)
# base
# Combo
# Absolute sum of number of element of d(..., :) *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)).
# reduce_percentage(input, percentage=0.5)
# base
# Combo
# Return the value of percentage in the sorted array: e.g., median value when percentage=0.5. Threshold: percentage="" (Default: 0.5) *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)).
# reduce_powersum(input, constant=2, precise=false)
# base
# Combo
# Sum of power, sum(power(x, constant)). Threshold: precise, whether calculate power precise if constant greater than 4, default false constant=, default:2 *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)).
# reduce_range(input)
# base
# Combo
# Return the range of values in the array, return NAN if no valid value *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)).
# reduce_skewness(input)
# base
# Combo
# Skewness of values in the array *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)).
# reduce_stddev(input, threshold=0)
# base
# Combo
# Standard deviation of values in the array. Threshold: Minimum required percentage of valid (non-nan) values. If there is not enough valid values, then the output is NAN. 0 means no limit.threshold (Default: 0) *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)).
# reduce_sum(input)
# base
# Combo
# Sum the number of element of d(..., :) *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)).
# """

# memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
# memory.chat_memory.add_ai_message(operator_reference)

# # Import all three execution tools
# from tools.executor import execute_python_code, execute_cpp_code, execute_java_code

# def create_agent(model_name: str = "gemini-1.5-flash-latest", temperature: float = 0.0, verbose: bool = True):
#     """
#     Creates and returns a LangChain agent executor for debugging code.
#     """
#     llm = ChatGoogleGenerativeAI( 
#         model=model_name,
#         temperature=temperature,
#         google_api_key=os.getenv("GOOGLE_API_KEY")
#     )

#     # The agent now has a tool for each language
#     tools = [execute_python_code, execute_cpp_code, execute_java_code]

#     prompt = hub.pull("hwchase17/react")

#     agent = create_react_agent(llm, tools, prompt)

#     agent_executor = AgentExecutor(
#         agent=agent,
#         tools=tools,
#         verbose=verbose, 
#         memory=memory,
#         handle_parsing_errors=True,
#         max_iterations=10
#     )
#     return agent_executor 
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub

import time
from collections import deque

# Import all three execution tools
from tools.executor import execute_python_code, execute_cpp_code, execute_java_code

def create_agent(model_name: str = "gemini-1.5-flash-latest", temperature: float = 0.0, verbose: bool = True):
    """
    Creates and returns a LangChain agent executor for debugging code.
    """
    llm = ChatGoogleGenerativeAI( 
        model=model_name,
        temperature=temperature,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    # The agent now has a tool for each language
    tools = [execute_python_code, execute_cpp_code, execute_java_code]

    prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=verbose, 
        handle_parsing_errors=True,
        max_iterations=15
    )
    return agent_executor 

class UsageTracker:
    def __init__(self, req_limit_per_day = 1000, req_limit_per_min = 120, token_limit_per_min = 1_800_000):
        self.req_limit_per_day = req_limit_per_day
        self.req_limit_per_min = req_limit_per_min
        self.token_limit_per_min = token_limit_per_min

        self.last_day = time.strftime("%Y-%m-%d")
        self.req_timestamps = deque()
        self.token_timestamps = deque()
        self.daily_requests = 0

    def record_usage(self, tokens_used):
        now = time.time()
        
        # Check date changes
        today = time.strftime("%Y-%m-%d")
        if today != self.last_day :
            self.daily_requests = 0
            self.last_day = today
            print("🔄Daily usage reset")

        # Record request timestamp
        self.req_timestamps.append(now)
        self.daily_requests += 1

        # Record tokens
        self.token_timestamps.append((now, tokens_used))

        # Cleanup old entries (older than 60s)
        while self.req_timestamps and now - self.req_timestamps[0] > 60:
            self.req_timestamps.popleft()

        while self.token_timestamps and now - self.token_timestamps[0][0] > 60:
            self.token_timestamps.popleft()

        # Compute current usage
        req_per_min = len(self.req_timestamps)
        tokens_per_min = sum(t for _, t in self.token_timestamps)

        # Warnings
        if req_per_min > self.req_limit_per_min * 0.8:
            print(f"⚠️ Approaching rate limit: {req_per_min}/{self.req_limit_per_min} req/min")

        if self.daily_requests > self.req_limit_per_day * 0.8:
            print(f"⚠️ Approaching daily limit: {self.daily_requests}/{self.req_limit_per_day} req/day")

        if tokens_per_min > self.token_limit_per_min * 0.8:
            print(f"⚠️ Approaching token limit: {tokens_per_min}/{self.token_limit_per_min} tokens/min")

        # Hard stops (optional)
        if req_per_min > self.req_limit_per_min:
            raise RuntimeError("🚫 API rate limit (requests/min) exceeded!")

        if self.daily_requests > self.req_limit_per_day:
            raise RuntimeError("🚫 Daily API request limit exceeded!")

        if tokens_per_min > self.token_limit_per_min:
            raise RuntimeError("🚫 Token usage limit exceeded!")

        return req_per_min, tokens_per_min
