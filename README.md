# Location Finder Web App

Web App to display images curated from Instagram that have no geo-tagging on them to be able to find their locations and display as a result.

The following steps are taken to collect data, train the model, find applications on untagged images and create an app:
1) **Training and test data collection**: training_data_collection.ipynb contains the code used to generate training and test data. While extracting images, geo-tag of image location, number of likes are also collected.
2) **Extract latitude and longtitude for addresses**: Once we have location link for the images that are geo-tagged, we extract the latitude, longitude from page source of Instagram page using BeautifulSoup. These lat,long are then fed to geopy to extract city_name, state name. The code is stored in extract_latitude_longitude_from_address.ipynb.
3) **Training Model**: VGG-16 model trained on ImageNet is leveraged with the last two layers retrained to classify 7 classes of scenaries - Mountain, Glacier, Geyser, Road, People, Sea, Northern Lights. The model is trained and stored in HDF5 file and reused later for prediction and visualization purposes. Each picture that was extracted in Step 1 is classified using this model and classes are stored in local files.
4) **Visualizing model layers**: CNN network trained in Step 3 is visualized using code from 'Visualizing and Understanding
Convolutional Networks' research paper by 'Matthew D. Zeiler and Rob Fergus'. The code is present in visualizing_vgg_16_layers.ipynb where the output gives images of each filter in 5 blocks of CNN layers and it is apparent which filter focuses on what aspects of images.
5) **Predicting Searching Images**: We need to find top 3 images closest to the query image and return their stored locations as a result. The code can be found in 'finding_locations_matching_untagged_images_on_instagram.ipynb'.

The app is deployed using Heroku and can be accessed here: *https://dry-mountain-96772.herokuapp.com/*

### Guidelines on using the app are below:

#### Landing Page:
![Landing Page](/static/images/Screenshot_1.png)

On the landing page, click on the image of which you want to find location. When you click, a green border appears on the image. Click on the 'Find Location' button and you will be able to find the locations of 3 most similar images to selected picture

#### Result Page:
![Result Page](/static/images/Screenshot_2.jpg)

On submitting the request, top 3 images are shows with their locations below which can be a possible location of the image.

#### Another example:
![Result 2](/static/images/Screenshot_3.png)

Sometimes, the app doesnt react fast enough and you might have to select the same picture again to get the relevant result. Please bear with it!





