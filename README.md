# Generic Buy Now, Pay Later Project
**Co-authors: Lang (Ron) Chen, Un Leng (Anderson) Kam, Yujie Li, Qirui (Cindy) Li, Haiyang (Henry) Huang**

***To best understand our work please download our [presentation](https://github.com/TGChenZP/MAST30034-A2_GroupWork__Py/blob/main/presentables/final%20presentation/ADS%20Group8%20Presentation%20Slides.pptx) at `/presentables/final presentation/ADS Group8 Presentation Slides.pptx`. Feel free to follow along with our provided [presentation script](https://github.com/TGChenZP/MAST30034-A2_GroupWork__Py/blob/main/presentables/final%20presentation/BNPL%20Presentation%20Script.pdf).***

<p align="center">
<img src="https://github.com/MAST30034-Applied-Data-Science/generic-buy-now-pay-later-project-group-8/blob/main/plots/bnpl_logo.jpg" class="centerImage" width="450" height="300">
<p>



## Guide
- [Summary Notebook](#summary-notebook)
- [Project Structure](#project-structure)
- [Weekly Checkpoints](#weekly-checkpoints)

---

**NOTE: IF ANY OF THE FILE PATHS FAIL TO LOAD, PLEASE GO TO https://drive.google.com/drive/folders/1h06sqKer80KU0lTFfRIPU61o6BZrk2qh?usp=sharing AND DOWNLOAD THE ENTIRE 'data' FOLDER AND REPLACE WITH CURRENT**

---

## Summary Notebook
`26_A_R_summary_notebook.ipynb` summarizes our group's solution to the BNPL problem, and presents findings.

## Project Structure
Please run the following files **in-order**, to ensure correct outputs.

### ETL and external data
- 1.  `1_A_ETL_script.py`: Join the desired trasaction dataset and returns a cleaned joined dataset, containing all merchant, consumer and transaction information.          
- 2.  `2_H_Download.py`: Download the external datasets and store it in ./data/raw/external_datasets.            

**Note:** For the ETL script, please enter the desire transaction snapshot, to run `4_A_simple_analysis.ipynb`

### EDA
- 3.  `3_A_understand_data.ipynb`: Provide a quick inspection on the provided transaction related datasets.
- 4.  `4_A_simple_analysis.ipynb`: Perform a simple analysis on the provided datasets, tries and deal with null values.
- 5.  `5_A_fraud_data_quick_look.ipynb`: Provide a quick inspection on the provided fraud related datasets.

### Fraud
- 6.  `6_R_C_fraud_inspect.ipynb`: Provide a quick inspection on the provided fraud related datasets, with descriptive statistics.
- 7.  `7_R_C_fraud_data_clean.ipynb`: Generate the dataset of engineered features required for training the fraud detector models.
- 8.  `8_R_C_fraud_model_consumer.ipynb`: Test different regression models to construct a consumer fraud detector.
- 9.  `9_R_C_fraud_model_merchant.ipynb`: Test different regression models to construct a merchant fraud detector.
- 10. `10_R_C_RFR consumer.ipynb`: Tune the consumer fraud detector model.
- 11. `11_R_C_consumer runthrough.ipynb`: Run the consumer fraud detector model on the full transaction dataset, and remove transaction data according to analysed boundaries.


### Basic Feature Engineering
- 12. `12_R_aggregate_transact_data_withTakeRate.ipynb`: Conduct aggregation to group transaction data to fortnights which outputs datasets required for notebooks below, and output the first three features for our final model.  

**Note:** the second half of the notebook uses imputed missing take rates - an output of clustering. But clustering used outputs from the first half of the notebook. **SO**: please run up to the line, and then run the clustering scripts, then come back to re-run the whole R_9 file.


### Clustering (for missing take rate imputation AND task of creating 3-5 separate business classes)
- 13. `13_H_Y_A_cluster_data_prep.ipynb`: Prepare clustering datasets.
- 14. `14_H_Y_A_cluster.ipynb`: Conduct clustering for take rate imputation and segmentation.
- 15. `15_C_tally_merchant_cluster.ipynb`: Generate an overview of the merchants in the clusters.
- 16. `16_C_marginal_dist_cluster.ipynb`: Plot the marginal distributions of the clusters to gain a better understanding for possible further analysis.
- 17. `17_R_combine_take_rate_and_imputed_take_rate.ipynb`: Fill in the merchants with missing take rates using the cluster result.


### Persona Score
- 18. `18_R_clean_occupation.ipynb`: Clean the occupation ABS dataset.
- 19. `19_R_postcode_total.ipynb`: Get frequency for each postcode of the cleaned occupation dataset.
- 20. `20_Y_income_clean.ipynb`: Clean the occupation income dataset.
- 21. `21_A_ranking_feature_engineering.ipynb`: Generate the 4th feature for the final model.
- 22. `22_Y_H_A_persona_score.ipynb`: Generate the 5th feature for the final model.


### Growth Rate (ultimately not used in modelw)
- 23. `23_C_R_future_return_prediction.ipynb`: Train the dateset to give future growth of a merchant revenue.
- 24. `24_C_R_get_growth.ipynb`: Predict the future growth of a merchant revenue.


### Final Model
- 25. `25_R_final_model.ipynb`: Train and test the final model, using the previous result, to generate the top 100 merchants to recommend to the BNPL firm.

## Weekly Checkpoints
Here indicates which notebooks are used to fullfil each weekly checkpoint according to provided specification.

- Sprint 1
  -  `1_A_ETL_script.py`    
  -  `2_H_Download.py` 

- Sprint 2
  -  `3_A_understand_data.ipynb`
  -  `4_A_simple_analysis.ipynb`
  - `13_H_Y_A_cluster_data_prep.ipynb`
  - `14_H_Y_A_cluster.ipynb`
  - `15_C_tally_merchant_cluster.ipynb`
  - `16_C_marginal_dist_cluster.ipynb`
  - `17_R_combine_take_rate_and_imputed_take_rate.ipynb`

- Sprint 3
  -  `5_A_fraud_data_quick_look.ipynb`
  -  `6_R_C_fraud_inspect.ipynb`
  -  `7_R_C_fraud_data_clean.ipynb`
  -  `9_R_C_fraud_model_merchant.ipynb`
  - `10_R_C_RFR consumer.ipynb`
  - `11_R_C_consumer runthrough.ipynb`

- Sprint 4
  - `12_R_aggregate_transact_data_withTakeRate.ipynb`  
  - `18_R_clean_occupation.ipynb`
  - `19_R_postcode_total.ipynb`
  - `20_Y_income_clean.ipynb`
  - `21_A_ranking_feature_engineering.ipynb`
  - `22_Y_H_A_persona_score.ipynb`
  - `23_C_R_future_return_prediction.ipynb`
  - `24_C_R_get_growth.ipynb`

- Sprint 5
  - `14_H_C_A_cluster.ipynb`

- Sprint 6
  - `25_R_final_model.ipynb`

- Sprint 7 
  - `26_A_R_summary_notebook.ipynb`
