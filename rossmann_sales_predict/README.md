![rossmann_logo](https://user-images.githubusercontent.com/68928802/137392417-f320ce54-6198-475a-9e15-ec0f3d4b162d.jpg)


# Rossmann Store Sales Prediction

##### Disclaimer 1
This is a fictitious context done with portfolio purpose. All the characters were created, as well the business problem.

##### Disclaimer 2
The data was published in a [kaggle competition](https://www.kaggle.com/c/rossmann-store-sales/overview).

##### Disclaimer 3
This project is part of the [Comunidade DS](https://sejaumdatascientist.com/inscricao-lives-comunidade-ds).

___

## Context

Rossmann is one of the largest drug store chains in Europe with 50k+ of employees and 4k+ stores.
However, the growth shown during the annual meeting where the regional managers present the sales plan for the next year to the CEO it is not compatible with Rossmann's greatness. So, in order to establish a new metric to measure the sales performance, the CEO asked the data manager for a sales prediction of the next year. As the growth projected by the sales teams is just a mean of the past sales.

But, after the kick-off meeting with the CEO where more questions about the problem were made we agreed that a full year prediction do not give us time to react a bad news. And also, the results will be reported quarterly, what makes a full year prediction useless. Therefore, was decided that a 6 weeks prediction will fit better into this scenario. It will be possible to notice significant variances and act to minimize the lost if necessary.

## Solution

So, from now on a challenge is settled, create this prediction to be used as a guideline to the annual sales plan. It will avoid losts and increase the gain with early decisions.

### Planning

##### Input

Three dataset:
- train.csv -> a dataset with historical sales
- store.csv -> suplemental info about the stores
- test.csv  -> a dataset with data about the next days

##### Output

Easy info with the prediction for the next 6 weeks

##### Tasks

1. Data Description:
  - Some basic info about the dataset such as dimensions, data types and also missing values
  - outliers check out
  - statistical description
  - Missing values treatment:
![Screenshot from 2021-10-13 20-37-50](https://user-images.githubusercontent.com/68928802/137227124-f107afed-948c-4700-918c-49482940499e.png)

2. Feature Engineering:
  - Mind map of hypothesis
  - feature creation
3. Exploratory Data Analysis:
  - Univatiated to check the features distribution
  - Bivariated, this step allowed me to check the behaviour of the features when working with the sales
    - It is also possible to validate the hypothesis created with the mind map
    - Some important hypothesis:

Store with close competition should sell less -> **FALSE**
![Screenshot from 2021-10-13 21-28-09](https://user-images.githubusercontent.com/68928802/137230723-1d8568a2-df46-43af-a1e8-50b81dcb5a3d.png)

Store should sell more after the 10th day of each month -> **TRUE**      
![Screenshot from 2021-10-13 21-13-53](https://user-images.githubusercontent.com/68928802/137230048-df39c14e-a605-4591-a13d-2caa03fddf8d.png) 

Store should sell more after the 10th day of each month -> **TRUE**      
![Screenshot from 2021-10-13 21-18-39](https://user-images.githubusercontent.com/68928802/137230050-33aeb018-e2b9-4c96-861c-a2b3e4ce4163.png)

4. Data Preparation
  - Data rescale with robust and min max scaler with pickle, to avoid data leak in production
  - Label Encoding
  - Nature Transform of time features

5. Feature Selection
  - Data split into 6 weeks blocks to make easier the cross training
  - feature selection with Botura

6. Machine Learning Modeling
  - Some modelings were tested:
    - Average model (baseline)
    - Linear regression
    - Linear regression regularized (Lasso)
    - Random forest regressor
    - XGBoost regressor
  - Metrics used to measure performance
    - MAE
    - MAPE
    - RMSE

Even though XGBoost is has not best performance it was chosen because is smaller and flexible when it comes to fine tuning.

![Screenshot from 2021-10-13 21-49-03](https://user-images.githubusercontent.com/68928802/137232262-7f3066de-06a0-4996-98a3-656a341f7f33.png)

7. Fine Tunning
  - Random Search was used.

Result after the fine tuning
![Screenshot from 2021-10-13 22-08-41](https://user-images.githubusercontent.com/68928802/137233626-13a8b0b4-9207-4aa0-98f2-82e5ae1b32ee.png)

8. Error Translation

  - Top 5 predictions 

![Screenshot from 2021-10-14 09-34-31](https://user-images.githubusercontent.com/68928802/137318676-be260f4f-161e-4a32-85d7-0ebd68354295.png) 

  - Predictions and sales along the 6 weeks and error rate, where y axis = 1 is like 0% of error 

![Screenshot from 2021-10-14 09-35-41](https://user-images.githubusercontent.com/68928802/137318682-6d58e530-b50b-4049-849e-1fb8b0ec2f28.png)

  - Absolute error dispersion 

![Screenshot from 2021-10-14 09-36-01](https://user-images.githubusercontent.com/68928802/137318685-3c180e88-4b94-4798-9e96-e3762358f5bb.png)


9. Telegram Bot
  - To access it, just click below 

[<img alt="Telegram" src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/>](https://t.me/das_rossmann_bot)

  - How to use it:
    - choose one of the command options below and send it to the bot

![Screenshot from 2021-09-29 21-20-13](https://user-images.githubusercontent.com/68928802/137385998-b978c56b-4776-4599-993b-888aa8109a3d.png)


## Next Steps
- Algorithm
  - In the next cycle new features such as holidays will be tested.
  - Also, a random forest regressor will be tested.
- Business
  - CEO and sales managers will follow this numbers closely and act accordingly with the real sales numbers.

## Lessons Learned
The main learning with this project is that it is important to plan the solution step by step. Respecting the order things should happen. Take a deep breath and understand the problem before start coding is the key. 

I also learned that a project is made in cicles, I will not create the perfect solution at the right first try.
Technically, I learned how to analyse data and prepare it to the modeling step. To do it, I used python and its libraries such as Pandas, Numpy, Matplotlib, Seaborn and many others. 

Modeling also needs attention, as it can overfit or even underfit if you do not read the errors carefully. Trying different regressor models allow me to compare then and see what I can improve in next cycle.
And last but not least, deploy this solution with flask, heroku and telegram bot was a very satisfying way to finish this great project.


Thank you for reading this project.
Any doubt or suggestion, just contact me:

[<img alt="Denny Profile" src="https://img.shields.io/badge/-LinkedIn-blue?style=for-the-badge&logo=linkedin"/>](https://linkedin.com/in/dennydaspinelli)
