![image](https://user-images.githubusercontent.com/68109182/215862568-4fabee03-e339-4e73-94a6-76d37d6bf572.png)

# Building Equity Market Data Analysis Pipeline
**[Step 1: Database Table Design](https://github.com/shrirupdwivedi/Springboard/blob/main/Capstone%202/%20Database_Table_Design.png)**

-Implement database tables to host the trade and quote data.

- Since trade and quote data is added on a daily basis with high volume, the design needs
to ensure the data growth over time doesn’t impact query performance. Most of the
analytical queries operate on data within the same day.

**[Step 2: Data Ingestion](https://github.com/shrirupdwivedi/Springboard/tree/main/Capstone%202/Step2_Data_Ingestion)**

- The source data comes in JSON or CSV files, which will be specified by file name
extension.

- Each file is mixed with both trade and quote records. The code needs to identify them by
column rec_type: Trade is “T”, Quote is “Q”.

- Exchanges are required to submit all their data before the market closes at 4 pm every
day. They might submit data in multiple batches. Your platform should pre-process the
data as soon as they arrive.

- The ingestion process needs to drop records that do not follow the schema.

**[Step 3: End of Day (EOD) Batch Load](https://github.com/shrirupdwivedi/Springboard/tree/main/Capstone%202/Data_Load)**

- Loads all the progressively processed data for current day into daily tables for trade and
quote.

- The Record Unique Identifier is the combination of columns: trade date, record type,
symbol, event time, event sequence number.

- Exchanges may submit the records which are intended to correct errors in previous ones
with updated information. Such updated records will have the same Record Unique
Identifier, defined above. The process should discard the old record and load only the
latest one to the table.

- Job should be scheduled to run at 5pm every day.

**[Step 4: Analytical ETL Job](https://github.com/shrirupdwivedi/Springboard/tree/main/Capstone%202/Step4:Analytical_ETL)**

To help the business teams do better analysis, we need to calculate supplement information for
quote records. Spring Capital wants to see the trade activity behind each quote. As the platform
developer, we are required to provide these additional results for each quote event:

- The latest trade price before the quote.

- The latest 30 min moving average trade price before the quote.

- The bid and ask price movement (difference) from the previous day's last trade price.
For example, given the last trade price of $30, bid price of $30.45 has a movement of
$0.45.
