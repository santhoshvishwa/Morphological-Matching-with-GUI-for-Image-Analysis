import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
from PIL import Image, ImageTk
import numpy as np

# Preprocessing Module
def preprocess_image(image_path):
    """
    Preprocess an image for feature extraction.
    Steps include resizing, grayscale conversion, Gaussian blurring, 
    and histogram equalization for better contrast.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")
    resized_image = cv2.resize(image, (256, 256))
    grayscale_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(grayscale_image, (5, 5), 0)
    enhanced_image = cv2.equalizeHist(blurred_image)
    return enhanced_image

# Feature Extraction Module
def extract_morphological_features(image):
    """
    Extract morphological features from an image using erosion, dilation,
    opening, and closing operations. These operations help in highlighting
    specific structural elements in the image, such as:
      - Erosion: Removes noise by eroding boundaries of objects.
      - Dilation: Enlarges bright regions, useful for filling gaps.
      - Opening: Removes small objects from the foreground.
      - Closing: Fills small holes in the foreground objects.
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    return {
        "Erosion": cv2.erode(image, kernel, iterations=1),
        "Dilation": cv2.dilate(image, kernel, iterations=1),
        "Opening": cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel),
        "Closing": cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    }

# GUI Application
class MorphologicalMatchingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Morphological Matching")
        self.root.geometry("1400x800")
        self.root.configure(bg="#f0f0f5")

        # State variables
        self.query_image_paths = []
        self.dataset_image_paths = []
        self.dataset_features_dict = {}
        self.query_features_list = []
        self.similarity_threshold = 5000  # Threshold value for similarity

        # Header Title
        tk.Label(root, text="Morphological Image Matching", font=("Helvetica", 18, "bold"), bg="#4B6FAE", fg="white",
                 padx=10, pady=10).pack(fill="x")

        # Buttons
        button_frame = tk.Frame(root, bg="#f0f0f5")
        button_frame.pack(pady=10)
        self.create_buttons(button_frame)

        # Query Image Frame
        self.query_frame_container = tk.LabelFrame(root, text="Query Images", bg="#c3d9ff", padx=10, pady=10)
        self.query_frame_container.pack(padx=10, pady=5, fill="x")

        self.query_canvas = tk.Canvas(self.query_frame_container, bg="white", height=150)
        self.query_scrollbar = tk.Scrollbar(self.query_frame_container, orient="horizontal", command=self.query_canvas.xview)
        self.query_scrollable_frame = tk.Frame(self.query_canvas, bg="white")

        self.query_canvas.create_window((0, 0), window=self.query_scrollable_frame, anchor="nw")
        self.query_canvas.configure(xscrollcommand=self.query_scrollbar.set)
        self.query_scrollable_frame.bind("<Configure>", lambda e: self.query_canvas.configure(scrollregion=self.query_canvas.bbox("all")))

        self.query_canvas.pack(side="top", fill="x")
        self.query_scrollbar.pack(side="bottom", fill="x")

        # Dataset Image Frame
        self.dataset_frame_container = tk.LabelFrame(root, text="Dataset Images", bg="#d9f9d9", padx=10, pady=10)
        self.dataset_frame_container.pack(padx=10, pady=5, fill="x")

        self.dataset_canvas = tk.Canvas(self.dataset_frame_container, bg="white", height=150)
        self.dataset_scrollbar = tk.Scrollbar(self.dataset_frame_container, orient="horizontal", command=self.dataset_canvas.xview)
        self.dataset_scrollable_frame = tk.Frame(self.dataset_canvas, bg="white")

        self.dataset_canvas.create_window((0, 0), window=self.dataset_scrollable_frame, anchor="nw")
        self.dataset_canvas.configure(xscrollcommand=self.dataset_scrollbar.set)
        self.dataset_scrollable_frame.bind("<Configure>", lambda e: self.dataset_canvas.configure(scrollregion=self.dataset_canvas.bbox("all")))

        self.dataset_canvas.pack(side="top", fill="x")
        self.dataset_scrollbar.pack(side="bottom", fill="x")

        # Scrollable Results Frame
        self.results_frame_container = tk.LabelFrame(root, text="Results", bg="#e6f7ff", padx=10, pady=10)
        self.results_frame_container.pack(padx=10, pady=10, fill="both", expand=True)

        self.results_canvas = tk.Canvas(self.results_frame_container, bg="white")
        self.scrollbar = tk.Scrollbar(self.results_frame_container, orient="vertical", command=self.results_canvas.yview)
        self.scrollable_frame = tk.Frame(self.results_canvas, bg="white")

        self.results_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.results_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame.bind("<Configure>", lambda e: self.results_canvas.configure(scrollregion=self.results_canvas.bbox("all")))
        self.results_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def create_buttons(self, parent):
        """
        Create and place buttons for uploading and processing images.
        """
        style = {"font": ("Helvetica", 12), "bg": "#4B6FAE", "fg": "white", "padx": 10, "pady": 5}
        tk.Button(parent, text="Upload Query Images", command=self.upload_query_images, **style).grid(row=0, column=0, padx=10)
        tk.Button(parent, text="Upload Dataset Images", command=self.upload_dataset_images, **style).grid(row=0, column=1, padx=10)
        tk.Button(parent, text="Calculate Similarity", command=self.calculate_similarity, **style).grid(row=0, column=2, padx=10)
        tk.Button(parent, text="Clear Results", command=self.clear_results, **style).grid(row=0, column=3, padx=10)

    def upload_query_images(self):
        """
        Upload and display multiple query images.
        Each image is preprocessed and its morphological features are extracted.
        """
        self.query_image_paths = filedialog.askopenfilenames(title="Select Query Images")
        self.query_features_list = []

        for widget in self.query_scrollable_frame.winfo_children():
            widget.destroy()

        for image_path in self.query_image_paths:
            preprocessed_image = preprocess_image(image_path)
            features = extract_morphological_features(preprocessed_image)
            self.query_features_list.append((image_path, features))
            self.display_thumbnail(self.query_scrollable_frame, image_path, size=(64, 64))
        messagebox.showinfo("Success", "Query images uploaded and processed successfully!")

    def upload_dataset_images(self):
        """
        Upload and display dataset images.
        Each image is preprocessed and its morphological features are extracted.
        """
        self.dataset_image_paths = filedialog.askopenfilenames(title="Select Dataset Images")
        self.dataset_features_dict = {}

        for widget in self.dataset_scrollable_frame.winfo_children():
            widget.destroy()

        for image_path in self.dataset_image_paths:
            preprocessed_image = preprocess_image(image_path)
            self.dataset_features_dict[image_path] = extract_morphological_features(preprocessed_image)
            self.display_thumbnail(self.dataset_scrollable_frame, image_path, size=(64, 64))
        messagebox.showinfo("Success", "Dataset images uploaded and processed successfully!")

    def calculate_similarity(self):
        """
        Calculate feature-wise similarity for all query and dataset image pairs.
        Display query images, dataset images, and their similarity results in the results window.
        """
        self.clear_results()

        thumbnail_size = (64, 64)  # Reduced thumbnail size
        for query_path, query_features in self.query_features_list:
            query_img = self.load_thumbnail(query_path, size=thumbnail_size)

            for dataset_path, dataset_features in self.dataset_features_dict.items():
                dataset_img = self.load_thumbnail(dataset_path, size=thumbnail_size)

                result_frame = tk.Frame(self.scrollable_frame, bg="white", padx=5, pady=5, relief="solid", borderwidth=1)
                result_frame.pack(pady=10, fill="x")

                query_label = tk.Label(result_frame, image=query_img, text="Query", compound="top", bg="white")
                query_label.image = query_img
                query_label.pack(side="left", padx=5, pady=5)

                dataset_label = tk.Label(result_frame, image=dataset_img, text="Dataset", compound="top", bg="white")
                dataset_label.image = dataset_img
                dataset_label.pack(side="left", padx=5, pady=5)

                # Generate similarity results
                results_text = f"Similarity Results:\n"
                for feature in query_features.keys():
                    distance = np.linalg.norm(query_features[feature].flatten() - dataset_features[feature].flatten())
                    similarity_status = "Similar" if distance <= self.similarity_threshold else "Not Similar"
                    results_text += f"{feature}: {distance:.2f} ({similarity_status})\n"

                # Display similarity results
                result_label = tk.Label(result_frame, text=results_text, justify="left", bg="white", font=("Helvetica", 10))
                result_label.pack(side="left", padx=10, pady=10)

    def display_thumbnail(self, parent, image_path, size=(128, 128)):
        """
        Display image thumbnails in the specified parent frame.

        Args:
            parent (tk.Widget): The parent widget where the thumbnail will be displayed.
            image_path (str): The file path of the image to be displayed.
            size (tuple): The size (width, height) of the thumbnail to be displayed.

        Purpose:
            Provides a visual representation of uploaded images, making it easier to correlate query and dataset entries.
        """
        img = cv2.imread(image_path)
        img = cv2.cvtColor(cv2.resize(img, size), cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(img))
        label = tk.Label(parent, image=img, bg="white")
        label.image = img
        label.pack(side="left", padx=5, pady=5)

    def load_thumbnail(self, image_path, size=(128, 128)):
        """
        Load an image as a thumbnail for display purposes.

        Args:
            image_path (str): The file path of the image to load.
            size (tuple): The size (width, height) of the thumbnail to create.

        Returns:
            ImageTk.PhotoImage: A photo image object for rendering in the GUI.
        """
        img = cv2.imread(image_path)
        img = cv2.cvtColor(cv2.resize(img, size), cv2.COLOR_BGR2RGB)
        return ImageTk.PhotoImage(Image.fromarray(img))

    def clear_results(self):
        """
        Clear the results display in the results frame.

        Purpose:
            Ensures the results frame is reset before a new similarity calculation is performed.
        """
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = MorphologicalMatchingApp(root)
    root.mainloop()
