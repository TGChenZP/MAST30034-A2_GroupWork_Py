# Generic Buy Now, Pay Later Project
Groups should generate their own suitable `README.md`.

Note to groups: Make sure to read the `README.md` located in `./data/README.md` for details on how the weekly datasets will be released.


**Notebooks**

ETL and external data
./scripts/
- 1. ETL_script.py            checkpoint: merge original dataset
- 2. Download.py              checkpoint: download external data using script

EDA + first inspect of data
- 3. A_1_simple_analysis.ipynb
- 4. A_1_understand_data.ipynb
- 5. A_2_fraud_data_quick_look.ipynb

Fraud
- 6. R_C_3_fraud_inspect.ipynb
- 7. R_C_4_fraud_data_clean.ipynb
- 8. R_C_5_fraud_model_consumer.ipynb
- 9. R_C_6_fraud_model_merchant.ipynb
- 10. R_C_7_RFR consumer.ipynb
- 11. R_8_consumer runthrough.ipynb

Basic Feature Engineering
- 12. R_9_aggregate_transact_data_withTakeRate.ipynb  #TODO: 改input file generate时候的output
    Note: the second half of the notebook uses imputed missing take rates - an output of clustering. But clustering used outputs from the first half of the notebook. SO: please run up to the line, and then run the clustering scripts, then come back to rerun the whole R_9 file.

Clustering (for missing take rate imputation AND task of creating 3-5 separate business classes)

Persona Data


Growth Rate
- . R_C_11_future_return_prediction.ipynb
- . R_12_get_growth.ipynb
- (Not included: C_7 which was a backup plan for R_12_get_growth.ipynb)

Final Model
- . R_13_final_model.ipynb