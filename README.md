# Multivariate CWRU Bearing Package
This package is created to extract and preprocess the CWRU Bearing datasets provided by the [Case Western Reserve University][cwru].
This package functions as an extension on the original package developed by [Litchiware][Litchiware], specifically designed to extract multivariate signals from the Bearing datasets for using in fault diagnosis experiments. Please read the documentation carefully for correct use of the package. 
### Installation
Installing the package can be done manually, but I recommend to install via pip since this is much easier by just copying the code below and paste it in your terminal/command prompt:
```sh
$ pip install multivariate-cwru
```

### Use of the package
After the installation, the package can be imported in your specific session, for example in Jupyter Notebook;
```sh
import multivariate_cwru
```
Then the class in the package can be called as follows;
```sh
data = multivariate_cwru.CWRU("12FanEndFault", 2048, 0.8, 1,2,'1797',normal_condition = True)
```
The called function results in six different objects:
* data.x_train, contains train samples represented in a 3D-array (nr of time series, sequence length, amount of sensors). 
* data.y_train, train labels representing different fault conditions.
* data.x_test, test samples, 3D-array (nr of time series, sequence length, amount of sensors). 
* data.y_test, test labels representing different fault conditions
* data.nclasses, amount of different fault conditions
* data.labels, the different fault conditions extracted from the datafiles

### Arguments
As can be seen in the previous code block, the package asks seven arguments for extracting and preprocessing the CWRU bearing datasets into usable objects. The following arguments need to be addressed when using CWRU class:
>1) Experiment: The specific name for the experiment to use. There are three options: `"12DriveEndFault"`, `"12FanEndFault"` and `"48DriveEndFault"`.
>2) Length: Sequence length of every time series.
>3) Trainsplit: Between 1 and 0 which splits the data into a train and test set.
>4) Seed: Set seed for data shuffle to recreate reproducible objects.
>5) Sens: number of sensors to be extracted. Integer number between  `1` and `3`.
>6) RPM: Choose the rotations per minute to narrow down the experiment's data. Four options are available, `"1797"`,`"1772"`,`"1750"`and `"1730"`. Multiple inputs are possible.
>7) Normal_condition: Boolean expression to add/exclude the normal conditions from the objects.










[cwru]: <https://csegroups.case.edu/bearingdatacenter/pages/welcome-case-western-reserve-university-bearing-data-center-website>
[Litchiware]: <https://github.com/Litchiware/cwru>





