## Personality Prediction of Instagram Users

This repository presents our end-of-year project: Personality Prediction of Instagram Users. We developed deep learning multi-label models to predict the OCEAN personality traits.

### Project Overview

1. **Data Collection**:
   - Using the Meta Developer Graph API Explorer, we gathered post URLs, captions, and dates from public profiles.
   - Stored the data in JSON files, which were then converted to CSV format.
   - Stored the images in a shared drive.

2. **Data Preparation**:
   - Normalized and resized images.
   - Cleaned textual data by removing stop words, special characters, annotations, and URLs.
   - Converted emojis to text, separated hashtags, and added new attributes (e.g., frequency and length of captions, number of mentions, and hashtags).

3. **Data Analysis**:
   - Visualized data distribution.
   - Created a correlation matrix.
   - Analyzed dependencies between attributes and personality traits.

4. **Model Development**:
   - **Image-Based Models**:
     - Simple CNN
     - CNN based on pretrained VGG16
     - CNN based on pretrained ResNet18
   - **Text-Based Models**:
     - BERT tokenization
     - Data augmentation via translation (English to French and back to English)

5. **Model Evaluation**:
   - Used confusion matrices for each label.
   - Calculated macro, micro, and weighted metrics (accuracy, F1 score, recall).

6. **Deployment**:
   - Implemented a Flask application/dashboard for real-time testing and deployment of the models.

### Project Structure

- **data/**: Contains the collected data.
- **models/**: Lists the trained models.
- **modules/**: Includes the steps of the project:
  - **data_collection/**: Data preparation and web scraping.
  - **data_analysis/**: Visualization.
  - **models_training/**: Training scripts for image-based (CNN/VGG16/ResNet18) and text-based (BERT) models.

This project  was  made  by a group of INSAT Students and  Data Science and Deep Learning Enthusiasts.
