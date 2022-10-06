# Generic Buy Now, Pay Later Project
Groups should generate their own suitable `README.md`.

Note to groups: Make sure to read the `README.md` located in `./data/README.md` for details on how the weekly datasets will be released.


**Notebooks**

ETL and external data
./scripts/
- 1. 1_A_ETL_script.py            checkpoint: merge original dataset
- 2. 2_H_Download.py              checkpoint: download external data using script

EDA + first inspect of data
- 3. 3_A_understand_data.ipynb
- 4. 4_A_simple_analysis.ipynb
- 5. 5_A_fraud_data_quick_look.ipynb

Fraud
- 6. 6_R_C_fraud_inspect.ipynb
- 7. 7_R_C_fraud_data_clean.ipynb
- 8. 8_R_C_fraud_model_consumer.ipynb
- 9. 9_R_C_fraud_model_merchant.ipynb
- 10. 10_R_C_RFR consumer.ipynb
- 11. 11_R_C_consumer runthrough.ipynb


Basic Feature Engineering
- 12. 12_R_aggregate_transact_data_withTakeRate.ipynb  #TODO: 改input file generate时候的output
    Note: the second half of the notebook uses imputed missing take rates - an output of clustering. But clustering used outputs from the first half of the notebook. SO: please run up to the line, and then run the clustering scripts, then come back to rerun the whole R_9 file.


Clustering (for missing take rate imputation AND task of creating 3-5 separate business classes)
- 13. 13_H_C_A_cluster_data_prep.ipynb
- 14. 14_H_C_Acluster.ipynb
- 15. 15_C_tally_merchant_cluster.ipynb
- 16. 16_C_marginal_dist_cluster.ipynb
- 17. 17_R_combine_take_rate_and_imputed_take_rate.ipynb


Persona Data
- 18. 18_R_clean_occupation.ipynb
- 19. 19_R_postcode_total.ipynb
- 20. 20_Y_income_clean.ipynb
- 21. 21_A_ranking_feature_engineering.ipynb
- 22. 22_Y_H_A_persona_score.ipynb


Growth Rate
- 23. 23_C_R_future_return_prediction.ipynb
- 24. 24_C_R_get_growth.ipynb


Final Model
- 25. 25_R_final_model.ipynb