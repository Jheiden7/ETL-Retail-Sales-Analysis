# ETL-Retail-Sales-Analysis

**Dataset:** Online Retail II

**Repository:** UCI Machine Learning.

**Link:** https://archive.ics.uci.edu/dataset/502/online+retail+ii

**Description:** This online sales dataset contains all transactions made by a non-store, UK-based registered company between December 1, 2009, and December 9, 2011. Many of the company's customers are wholesalers.

**Associated Tasks:** Regression, classification, and clustering.

**Number of Attributes:** 8.

**Number of Observations:** 1,067,371.

**Attribute Information:**

| Variable      | Type        | Description                                                                                                                            |
|---------------|-------------|----------------------------------------------------------------------------------------------------------------------------------------|
| **Invoice**   | Categorical | A 6-digit integral number uniquely assigned to each transaction. If this code starts with the letter 'c', it indicates a cancellation.   |
| **StockCode** | Categorical | Product code. A 5-digit integral number uniquely assigned to each distinct product.                                                    |
| **Description**| Categorical | Product name.                                                                                                                          |
| **Quantity**  | Numeric     | The quantities of each product (item) per transaction.                                                                                 |
| **InvoiceDate**| Categorical | Invoice date and time. The day and time a transaction was generated.                                                                   |
| **Price**     | Numeric     | Unit price of the product in Pound Sterling (GBP).                                                                                     |
| **Customer ID**| Numeric     | A 5-digit integral number uniquely assigned to each customer.                                                                          |
| **Country**   | Categorical | The name of the country where a customer resides.                                                                                      |

**Business Understanding:** When managing a sales site, the goal as an entrepreneur is to increase profits, which translates to reaching more customers and/or increasing sales even if the number of customers remains the same. To achieve this, it is necessary to employ different market strategies, which in turn requires a rigorous study of the sector to understand market behavior according to country, customer, date, product, etc. For this reason, it is proposed to obtain different graphs that allow visualizing sales behaviors according to other parameters.

**Objective:** Perform data preprocessing to obtain the following graphs:

- **Sales vs. Country (Total, average, and cumulative by Stock Code):** This will allow us to identify the countries that make the most purchases, which could lead to decision-making when determining whether it is worthwhile to offer a product in a specific country.

- **Sales vs. Customer ID:** This will help identify the most valuable customers for the business, as it will show which individuals have the highest number of purchases. Knowing this, special offers or preferential treatment could be provided to retain them.

- **Sales vs. Date (Year-Month-Day and Year-Month):** This will reveal the dates and months of the year with the highest sales volume, or even identify periods with lower sales. This information will allow for the development of strategies to prepare for specific dates and find ways to boost sales.

- **Quantity vs. StockCode - For each month of the year:** This allows us to determine which products sell the most each month. For example, sunscreen might sell well in the summer, and toys in December. This way, the business can ensure maximum availability of these products as those dates approach, leading to a greater sales capacity.
