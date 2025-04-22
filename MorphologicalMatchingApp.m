classdef MorphologicalMatchingApp < handle
    % Define the main app class for morphological image matching with a GUI

    properties
        % UI Components
        Figure  % The main figure window for the app
        QueryCanvas  % Canvas to display the query image
        ResultsPanel  % Panel to display results
        ResultsPanelScrollable  % Scrollable layout for displaying results
        QueryImagePath   % Path of the uploaded query image
        DatasetImagePaths   % Paths of the uploaded dataset images
        QueryFeatures  % Extracted features of the query image
        DatasetFeatures  % Extracted features of the dataset images
        SimilarityThreshold = 5000;  % Similarity threshold value
    end
    
    methods
        % Constructor to initialize the UI elements
        function app = MorphologicalMatchingApp()
            % Create and configure the main figure for the app
            app.Figure = uifigure('Name', 'Morphological Matching');
            app.Figure.Position = [100, 100, 800, 600];
            
            % Create the button for uploading the query image
            uibutton(app.Figure, 'Text', 'Upload Query Image', ...
                'Position', [150, 550, 150, 30], ...
                'ButtonPushedFcn', @(btn, event) app.uploadQueryImage());
            
            % Create the button for uploading the dataset images
            uibutton(app.Figure, 'Text', 'Upload Dataset Images', ...
                'Position', [150, 500, 150, 30], ...
                'ButtonPushedFcn', @(btn, event) app.uploadDatasetImages());
            
            % Create the button to calculate the similarity
            uibutton(app.Figure, 'Text', 'Calculate Similarity', ...
                'Position', [150, 450, 150, 30], ...
                'ButtonPushedFcn', @(btn, event) app.calculateSimilarity());
            
            % Create the canvas to display the query image
            app.QueryCanvas = uiaxes(app.Figure);
            app.QueryCanvas.Position = [472, 430, 156, 156];
            
            % Create the scrollable results panel with two columns: images and text
            app.ResultsPanel = uipanel(app.Figure, 'Position', [60, 40, 650, 350]);
            app.ResultsPanelScrollable = uigridlayout(app.ResultsPanel, ...
                'Scrollable', 'on', ...
                'RowHeight', {'fit'}, ...
                'ColumnWidth', {'0.5x', '0.5x'});  % Two columns for images and text
        end
        
        % Method to upload and process the query image
        function uploadQueryImage(app)
            [filename, pathname] = uigetfile({'*.jpg;*.png;*.bmp', 'Image Files (*.jpg,*.png,*.bmp)'}); 
            if filename ~= 0
                app.QueryImagePath = fullfile(pathname, filename);
                preprocessedQuery = app.preprocessImage(app.QueryImagePath);
                app.QueryFeatures = app.extractMorphologicalFeatures(preprocessedQuery);
                
                % Display the query image in the canvas
                imshow(imread(app.QueryImagePath), 'Parent', app.QueryCanvas);
                
                % Show success message
                uialert(app.Figure, 'Query image uploaded and processed successfully!', ...
                    'Success', 'Icon', 'info');
            end
        end
        
        % Method to upload and process the dataset images
        function uploadDatasetImages(app)
            [filenames, pathname] = uigetfile({'*.jpg;*.png;*.bmp', 'Image Files (*.jpg,*.png,*.bmp)'}, ...
                'Select Dataset Images', 'MultiSelect', 'on');
            if ~isequal(filenames, 0)
                app.DatasetImagePaths = {};
                app.DatasetFeatures = struct();
                
                % Loop through each selected dataset image and process it
                if ischar(filenames)
                    filenames = {filenames};
                end
                for i = 1:length(filenames)
                    fullPath = fullfile(pathname, filenames{i});
                    app.DatasetImagePaths{end + 1} = fullPath;
                    preprocessedImage = app.preprocessImage(fullPath);
                    app.DatasetFeatures.(sprintf('image_%d', i)) = ...
                        app.extractMorphologicalFeatures(preprocessedImage);
                end
                % Show success message
                uialert(app.Figure, 'Dataset images uploaded and processed successfully!', ...
                    'Success', 'Icon', 'info');
            end
        end
        
        % Method to calculate similarity between query and dataset images
        function calculateSimilarity(app)
            if isempty(app.QueryFeatures)
                % Show error message if query features are not extracted
                uialert(app.Figure, 'Query features are not extracted. Upload a query image.', ...
                    'Error', 'Icon', 'error');
                return;
            end
            if isempty(app.DatasetFeatures)
                % Show error message if dataset features are not extracted
                uialert(app.Figure, 'Dataset features are not extracted. Upload dataset images.', ...
                    'Error', 'Icon', 'error');
                return;
            end
            
            % Calculate similarity between query and dataset images
            featurewiseResults = app.calculateFeaturewiseSimilarity();
            
            % Display the results
            app.displayResults(featurewiseResults);
        end
        
        % Method to calculate feature-wise similarity between query and dataset images
        function featurewiseResults = calculateFeaturewiseSimilarity(app)
            featurewiseResults = struct();
            featureNames = fieldnames(app.QueryFeatures);
            datasetNames = fieldnames(app.DatasetFeatures);
            
            % Loop through each dataset image and calculate similarity for each feature
            for i = 1:length(datasetNames)
                similarities = zeros(length(featureNames), 1);
                for j = 1:length(featureNames)
                    featureName = featureNames{j};
                    queryFeature = double(app.QueryFeatures.(featureName));
                    datasetFeature = double(app.DatasetFeatures.(datasetNames{i}).(featureName));
                    similarities(j) = norm(queryFeature(:) - datasetFeature(:));  % Euclidean distance
                end
                featurewiseResults.(datasetNames{i}) = similarities;  % Store results
            end
        end
        
        % Method to display the results in a scrollable panel
        function displayResults(app, featurewiseResults)
            % Clear previous results in the results panel
            delete(app.ResultsPanelScrollable.Children);
            
            % Determine the number of dataset images
            numResults = numel(app.DatasetImagePaths);
            
            % Adjust the layout for the result images and texts
            app.ResultsPanelScrollable.RowHeight = repmat({'fit'}, numResults, 1);
            
            % Loop through the dataset names and display each result
            datasetNames = fieldnames(featurewiseResults);
            for i = 1:length(datasetNames)
                if i > numResults
                    continue;  % Skip if the result exceeds the number of images
                end
                
                % Display dataset image in the first column
                img = uiimage(app.ResultsPanelScrollable, ...
                    'ImageSource', app.DatasetImagePaths{i}, ...
                    'ScaleMethod', 'fit');
                img.Layout.Row = i;
                img.Layout.Column = 1;  % Place in the first column for images
                
                % Format and display similarity result text in the second column
                resultText = sprintf('Similarity Results:\n');
                similarities = featurewiseResults.(datasetNames{i});
                featureNames = fieldnames(app.QueryFeatures);
                
                % Loop through similarities and format them into a result text
                for j = 1:length(similarities)
                    similarityText = 'Similar'; % Default text
                    if similarities(j) > app.SimilarityThreshold  % Check if similarity exceeds threshold
                        similarityText = 'Not Similar';
                    end
                    resultText = sprintf('%s%s: %.2f (%s)\n', resultText, featureNames{j}, similarities(j), similarityText);
                end
                
                % Display result text in the second column
                resultTextArea = uitextarea(app.ResultsPanelScrollable, ...
                    'Value', resultText, ...
                    'Editable', 'off', ...
                    'FontSize', 12, ...
                    'HorizontalAlignment', 'left');
                resultTextArea.Layout.Row = i;
                resultTextArea.Layout.Column = 2;  % Place in the second column for text
            end
        end
    end
    
    methods (Static)
        % Method to preprocess images: convert to grayscale, resize, blur, and equalize
        function enhanced = preprocessImage(imagePath)
            img = imread(imagePath);
            if size(img, 3) == 3
                img = rgb2gray(img);  % Convert RGB to grayscale
            end
            resized = imresize(img, [256, 256]);  % Resize image to 256x256
            blurred = imgaussfilt(resized, 2);  % Apply Gaussian blur
            enhanced = histeq(blurred);  % Histogram equalization
        end
        
        % Method to extract morphological features using various operations
        function features = extractMorphologicalFeatures(image)
            se = strel('rectangle', [3, 3]);  % Define a structural element (rectangle)
            features = struct();
            features.Erosion = imerode(image, se);  % Erosion
            features.Dilation = imdilate(image, se);  % Dilation
            features.Opening = imopen(image, se);  % Opening
            features.Closing = imclose(image, se);  % Closing
        end
    end
end

% Main function to run the app
function runApp()
    app = MorphologicalMatchingApp();  % Create and run the app
end
