# Morphological-Matching-with-GUI-for-Image-Analysis
Abstract

Fundamentally, with the rapid development of digital imaging, there is an urgent need for new methods to analyze and compare images. This paper represents the design and implementation of the morphological matching system with a graphical user interface. Conventionally, this system will enable users to query against visually similar images, which have morphological features such as erosion, dilation, opening, and closing within the large datasets of images. Implemented in Python, the system involves OpenCV for image processing, Tkinter for GUI development, and standard distance metrics for measuring similarity. The final system is robust and efficient and finds lots of potential applications in medical imaging, satellite image processing, and digital forensics.

1. Introduction

The ever-growing utilization of digital imaging within the domains of biology, medicine, material sciences, and forensic investigations has created a growing need for systems that get images analyzed and compared with respect to their structural properties. Morphological matching is a technique that appears to find similarities between pictures with respect to their shapes, structures, and patterns.
That is, in contrast with the currently utilized methods of image comparison, most of the time based on colour or texture, morphological matching focuses on structural characteristics through operations such as erosion, dilation, opening, and closing. This report presents the design, implementation, and evaluation of a morphological matching system, which has a very friendly GUI to enable researchers and professionals to easily retrieve images similar to one under query from large datasets.

2. Objectives
   
The main objectives of this project are:
i.	To establish a framework through which images can be processed and Compared concerning morphological attributes.
ii.	To incorporate a user interface for a choice of query images and datasets for interaction using GUI.
iii.	To incorporate proper algorithms such as preprocessing, feature vector production, and a measure of similarity.
iv.	Extensive data sets are needed to address some specific challenges that accompany the implementation of deep learning models for image recognition.

3. Methodology

3.1 Preprocessing

First, the morphological matching system preprocesses the images by preparing them for further processing. The idea here is that all photos in the dataset represent the same properties, which will ensure consistent and accurate morphological feature extraction.

The preprocessing commences with the resizing of images to a standard dimension of 256 x 256 pixels; hence, any size irregularities within the dataset are precluded. Following the resizing process, the images were converted into their respective grayscale versions, reducing the colour information in the analysis and focusing solely on structural or intensity variations.

Gaussian blur is conducted to reduce the overall noise, which would, in turn, remove minor irregularities and give a better view of significant structural details. Finally, histogram equalization is performed to enhance contrast, adjusting the distribution of intensities in the image so that the predominant features become better developed through enhanced morphological analysis.

These are essential preprocessing steps that lay the platform for feature extraction and similarity measurement accurately.

3.2 Feature Extraction

Morphological operations are an essential part of the subsystems, which are used for extracting the structural meaning features from images. These operations look for geometric characteristics in the image; their results differ from those based on pixel intensity and colour.

The first operation, erosion, reduces the size of the bright areas of an image by cutting off pixels on the boundary of the bright regions. This serves to help one define small but critical features while leaving out bothering structures outside the limit of visibility. On the other hand, expansion dilates the bright areas by adding distances around the outlines, making features more detectable and consolidating minor splits.

Opening is also an operation where erosion is applied first and then dilation. It is beneficial in erasing minor noise or unwanted speckles from the image and improving the visibility of the primary forms. In the same respect, closing, which uses the operation of dilation and then erosion, acts efficiently in the filling of minor gaps or holes that may be observed within the regions that are bright in the image, resulting in the enhancement of the continuity of the structures.

All these operations are made using structuring elements (kernels) of 5×5 in size. These kernels define the shape and scale of the morphological transformations, allowing the system to capture and analyze structural variations within the image effectively. This feature extraction process ensures that the most relevant morphological details are available for similarity measurement.

3.3 Similarity Measurement

For comparing images, the extracted features of the query image are matched against those of the dataset images using Euclidean distance. The distance is calculated for each morphological feature, and a feature-wise similarity score is generated. Lower distances indicate higher similarity.

Threshold Comparison:

The threshold is used to decide if two images are considered similar. If the calculated distance between features is less than or equal to 5000, the images are considered "Similar". If it's greater than 5000, the images are considered "Not Similar".

Python Implementation

def calculate_featurewise_similarity(query_features_dict, dataset_features_dict):
	featurewise_similarities = {}
	for image_name, dataset_features in dataset_features_dict.items():
    	similarities = {}
    	for feature_name in query_features_dict.keys():
        	distance = np.linalg.norm(
            	query_features_dict[feature_name].flatten() -
            	dataset_features[feature_name].flatten()
        	)
        	similarities[feature_name] = distance
    	featurewise_similarities[image_name] = sorted(
        	similarities.items(),
        	key=lambda x: x[1]
    	)
	return featurewise_similarities
MATLAB Implementation
function featurewiseResults = calculateFeaturewiseSimilarity(app)
	featurewiseResults = struct();
	featureNames = fieldnames(app.QueryFeatures);
    
	datasetNames = fieldnames(app.DatasetFeatures);
	for i = 1:length(datasetNames)
    	similarities = zeros(length(featureNames), 1);
    	for j = 1:length(featureNames)
        	featureName = featureNames{j};
        	queryFeature = double(app.QueryFeatures.(featureName));
        	datasetFeature = double(app.DatasetFeatures.(datasetNames{i}).(featureName));
        	similarities(j) = norm(queryFeature(:) - datasetFeature(:));
    	end
    	featurewiseResults.(datasetNames{i}) = similarities;
	end
 end

3.4 Graphical User Interface (GUI)

The GUI allows users to:

●	Upload a query image

●	Upload multiple dataset images

●	Compute and display similar results interactively

●	Visualize the morphological features of the query image

Python Implementation

The GUI is built using Tkinter, providing a lightweight and native interface.

MATLAB Implementation

The GUI is built using MATLAB App Designer, providing a rich, platform-independent interface with built-in visualization capabilities.

4. Implementation

Requirement Resources (Windows/Linux): 

The project can be implemented on both Windows and Linux platforms. Here are the specific resource requirements:

Hardware Requirements:

A computer system with at least 4 GB of RAM (8 GB recommended for larger datasets).
A dual-core processor or higher.
At least 10 GB of free disk space for storing datasets and dependencies.

Software Requirements:

Python (version 3.6 or higher) with necessary libraries:
OpenCV (for image processing)
Tkinter (for GUI development)
NumPy (for numerical computations)
PIL (for handling image formats in GUI)
MATLAB (for MATLAB implementation) with the Image Processing Toolbox.
Operating system: Windows 10/11 or Ubuntu 18.04 or higher.
Optional: Flask or Django for web-based deployment if future enhancements are needed.
Development Tools:

Integrated Development Environment (IDE): PyCharm, VSCode, or MATLAB App Designer for GUI creation.
Libraries for visualization and plotting (e.g., Matplotlib if visualization is needed in Python).

The project is implemented in both Python and MATLAB, utilizing their respective strengths:

Python Version

●	OpenCV: For image preprocessing and morphological operations

●	Tkinter: For GUI development

●	NumPy: For numerical computations, including similarity measurement

●	PIL: For image handling in the GUI

MATLAB Version

●	Image Processing Toolbox: For image preprocessing and morphological operations

●	App Designer: For GUI development

●	Built-in Functions: For numerical computations and similarity measurement

4.1 Workflow

1.	Upload Images: The user uploads a query image and dataset images through the GUI.

2.	Preprocessing: Images are resized, converted to grayscale, denoised, and contrast-enhanced.

3.	Feature Extraction: Morphological features (erosion, dilation, opening, and closing) are extracted for each image.

4.	Similarity Calculation: Feature-wise similarity scores between the query image and each dataset image are computed.

5.	Results Display: Similarity results are displayed in the GUI, sorted by feature-wise scores.

5. Results

5.1 GUI Overview

The system successfully processed a dataset containing five images and calculated feature-wise similarity scores based on critical morphological features. These features, which include erosion, dilation, opening, and closing, were computed for each image in the dataset relative to the query image. The results provide detailed similarity in structure between the query image and dataset images.

Erosion is a representation of the shrinkage of white areas in an image; thus, it allows subtle information to be extracted from the structure. In calculating the similarity scores for erosion, the system takes into consideration the shape and contour differences of white areas between images. In contrast, dilation, which is associated with the growth of white areas, exposes structural amplification, thereby ensuring that larger patterns are well-represented in the similarity analyses.

Opening, which comprises erosion followed by dilation, successfully removes slight noise from the images while retaining great structural features. Of this feature, only the Detect table is helpful in seeking clean, noise-free patterns in the dataset images. In contrast,_closure_, which applies dilation followed by erosion, brings back ‘lost’ pixel features within regions by regenerating narrow shapes within the bright areas and thus would allow the identification of more prominent, unbroken patterns.

The similarity scores for each of these operations were then shown with the corresponding images of the datasets in the feature-wise GUI. The ability to view the structural properties of the query image to those of the dataset images proves helpful in terms of assessing the morphological likeness and disparity. The results demonstrate that the system can perform detailed image analyses and enables good content-based image retrieval.

 Running Morphological Matching Application in MATLAB Online

Prerequisites

Before running the application in MATLAB Online, ensure the following requirements are met:

1. MATLAB Online Access
•	Access MATLAB Online through your MathWorks account.("https://matlab.mathworks.com/"
•	A valid license for MATLAB is required (academic or commercial).
2. Required Toolboxes
•	Confirm that the Image Processing Toolbox is available. To check for installed toolboxes in MATLAB Online, run the following command in the MATLAB Command Window:

"ver"

Ensure that the Image Processing Toolbox is listed in the output.

4. Supported Web Browser
•	Use the latest version of one of the following browsers:
o	Google Chrome
o	Mozilla Firefox
o	Safari
o	Microsoft Edge

5. Stable Internet Connection
•	MATLAB Online requires a reliable and high-speed internet connection to function properly.

7. Input Files
•	Have the following files ready for upload:
o	MorphologicalMatchingApp.m: The MATLAB application file.
o	One or more image files (.jpg, .png, .bmp) to use as the query and dataset images.

Step-by-Step Instructions to Run the Application

i. Upload Files to MATLAB Online
ii.	Log in to MATLAB Online: Go to MATLAB Online and log in using your MathWorks account.
iii.	Upload the Files:
iv.	Navigate to the Home tab in MATLAB Online.
v.	Click Upload and select the MorphologicalMatchingApp.m file.
vi.	Similarly, upload the image files that you plan to use.

Set the Current Folder
Ensure that the folder containing MorphologicalMatchingApp.m is set as the current directory. It can be done this by:
•	Using the Current Folder browser to navigate to the appropriate folder, or
•	Typing the following command in the MATLAB Command Window:
cd('path_to_the_folder')
Replace "path_to_the_folder" with the location where the MorphologicalMatchingApp.m file is uploaded.

Run the Application
1.	Open the MATLAB Command Window.
2.	Type the following command to launch the application:
"runApp"
3.	The application interface will appear.
4. Use the Application

Uploading a Query Image
•	Click the "Upload Query Image" button.
•	Select an image file from your local system.
•	The application will preprocess the image and display it in the query canvas. A success message will confirm the upload.

Uploading Dataset Images
•	Click the "Upload Dataset Images" button.
•	Select one or more image files from your local system.
•	The application will preprocess the images and store the extracted features. A success message will confirm the upload.

Calculating Similarity
•	Click the "Calculate Similarity" button.
•	The application will compute the feature-based similarity between the query image and dataset images.
•	Results, including similarity values for morphological features, will be displayed in the results panel.


5.3 Performance

The system was tested with datasets of variable sizes. Various preprocessing and feature extraction steps were done in order to optimize the performance so that the system can efficiently manage up to 100 images per dataset.

6. Applications

The developed system has a number of potential uses in numerous industries as a result of the algorithm’s capacity to process and compare images on the basis of shape.

In medical imaging, the system can be used to locate regions in diagnostic images that have pathological characteristics similar to those of other corresponding parts, such as X-ray, MRI, or CT images. This capability could help doctors to ‘see’ something abnormal or to track the progression of the diseases when surveying the structural patterns of different regions or different patients.

In satellite image processing, the system can then evaluate and compare morphological characteristics of geographic regions. This application is beneficial to knowing the alterations in the use of the land or urban growth or environmental modifications by aligning images from satellites that have similar structures.

Digital forensics is made easy by the system, which enables one to match images of the evidence. Thus, considering structural similarities can help investigators find similar photos, links, or patterns that are not easily recognizable when working with other analytic tools.

These applications demonstrate the system’s adaptability and proof of concept that it can be helpful in mission-critical analysis tasks in domains dependent on image processing.

7. Limitations and Future Work

7.1 Limitations

Currently, basic morphological features, dilation, opening, and closing, play a primary role in the implementation of the morphological matching system. These features were shown to perform as well as any other technique currently available for capturing structural properties; however, the system can be further enhanced in terms of robustness and accuracy by incorporating more advanced morphological features.

Other limitations include reliance on Euclidean distance as a measure of main similarity. Though computationally efficient and straightforward, this may not be effective in capturing perceptual similarities from images, especially for more complicated datasets or scenarios with non-linear relationships. The usage of more advanced metrics for distance is one sure way of overcoming these limitations.

While functional, the GUI could include enhanced visualizations and additional features to improve usability. For instance, more intuitive controls, better layouts, and interactive visualizations could make the interface much friendlier and more intuitive to execute for a wide array of users with less technical knowledge.

7.2 Future Work

These limitations have been identified, and several future improvements have been put forward. Firstly, in addition to the implemented similarity metrics such as SSIM, more could be implemented so that image comparison will always be both more accurate and perceptually more meaningful. SSIM takes into consideration structural information; hence, it is a better metric for many applications.

Support for batch processing of query images is another essential feature for improvement in the system. Currently, the system processes one query image at a time. Enhancement of the type of functionality able to let the user process multiple query images in batches would, therefore, be efficient in handling large datasets.

Finally, the system could be deployed as a web application using Flask or Django. A web-based interface would make the system more accessible to a wide range of users where interaction with the application via browser is allowed without installing it locally. It promotes scalability and integration with other available tools and platforms.

8. Conclusion

This project successfully designed a morphological matching system with a GUI that performs the intended image analysis. The aims of the system are acquitted in the realm of efficient preprocessing, feature extraction, measurement of similarity, and interaction with the user. The system can become very productive, with further refinement, in medicine, forensics, or geospatial studies. The power of morphological analysis in image processing was brought to the fore comprehensively in this project and provided a solid grounding for future research and development in this area.


References:

•	Giang Hong Nguyen 1,2 *, Yen Thi Hoang Hua 1,3, Linh Chi Nguyen 1,3, Liet Van Dang 1,3 “Image Enhancement Using Bidimensional Empirical Mode Decomposition and Morphological Operations for Brain Tumor Detection and Classification”.

•	A.M.Raid1 , W.M.Khedr2 , M.A.El-dosuky1 and Mona Aoud1 1 Mansoura University, Faculty of Computer Science and Information System 2 Zagazig University, Faculty of Science “IMAGE RESTORATION BASED ON MORPHOLOGICAL OPERATIONS”.

•	R. C. Gonzalez, R.E. Woods, “Digital Image Processing”, 2nd Edition. 

•	S. W. Smith, “Chapter 25: Special Imaging Techniques”.https://www.dspguide.com/ch25/4.htm 

•	Tekam M. “Morphological transformations for enhancement of images with poor contrast and detection of background. IJIREEICE. 2015;3:16-20. https://doi.org/10.17148/IJIREEICE.2015.31104”

•	Widyantara IM. “Image enhancement using morphological contrast enhancement for video based image analysis”. 2016.

•	 Hassanpour H, Samadiani N, Salehi SM. “Using morphological
transforms to enhance the contrast of medical images”. Egypt J Radiol Nucl Med. 2015;46:481-9. https://doi.org/10.1016/j.ejrnm.2015.01.004

•	https://www.geeksforgeeks.org/image-segmentation-using-morphological-operation/

•	https://stackoverflow.com/questions/56183201/detect-and-visualize-differences-between-two-images-with-opencv-python

•	https://www.mathworks.com/matlabcentral/fileexchange/24224-magic-matlab-generic-imaging-component
