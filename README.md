# R.E.B.E.C.C.A (Recognition of Essential Biological Elements in Chromosome Configuration Analysis)

## Project Overview

R.E.B.E.C.C.A is a cutting-edge project aimed at analyzing chromosomal images to identify the chromosomal count and detect potential genetic disorders in fetuses. Leveraging advanced deep learning techniques and image processing, the system provides accurate analysis, offering crucial insights for prenatal diagnostics.

## Features

- **Chromosomal Image Analysis**: Detect and classify chromosomes from microscopic images.
- **Chromosomal Count Identification**: Automatically count the number of chromosomes present in the image.
- **Genetic Disorder Detection**: Identify potential genetic disorders based on chromosomal configurations.
- **User Interface**: React-based front end for user interaction and result visualization.

## Tech Stack

### 1. **YOLOv8**
   - **Purpose**: YOLOv8 (You Only Look Once version 8) is employed for model generation. It powers the image recognition system by training on chromosomal images to accurately detect and classify chromosomes.
   - **Why YOLOv8**: YOLOv8 is optimized for real-time object detection, making it ideal for analyzing high-resolution chromosomal images efficiently.

### 2. **Python**
   - **Purpose**: Python is the primary programming language used for building the backend, integrating the YOLOv8 model, and handling image processing tasks.
   - **Libraries Used**: Key libraries include PyTorch (for model handling), OpenCV (for image processing), and NumPy (for numerical operations).

### 3. **React**
   - **Purpose**: React is used to build the frontend of the application. It provides a dynamic and responsive user interface where users can upload images and visualize the analysis results.
   - **Why React**: React's component-based architecture and efficient rendering make it ideal for handling dynamic user interactions and displaying complex data in a clear, user-friendly manner.

### 4. **TypeScript**
   - **Purpose**: TypeScript is utilized in conjunction with React to provide type safety, making the codebase more robust and easier to maintain.
   - **Why TypeScript**: By catching type-related errors early during development, TypeScript ensures a more reliable and scalable codebase.

## Flowchart

![Flowchart] (images/0.png)

## Results

![Results] (images/1.png)
![Results] (images/2.png)
![Results] (images/3.png)
![Results] (images/4.png)

## Application Deployment

The application is deployed as a React app. Here are the steps to set it up:

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/your-repo-url.git
   cd rebecca-project
   ```

2. **Install Dependencies**  
   Ensure you have Node.js installed. Then, run:
   ```bash
   npm install
   ```

3. **Run the App**  
   Start the development server:
   ```bash
   npm run dev
   ```
   The app will be live at `http://localhost:3000`.

4. **Build for Production**  
   To build the app for production, run:
   ```bash
   npm run build
   ```

5. **Deploy**  
   You can deploy the production build to any static hosting service, such as Vercel, Netlify, or GitHub Pages.

## Future Enhancements

- **Enhanced Disorder Detection**: Expand the genetic disorder detection capabilities with more comprehensive training data.
- **Real-time Processing**: Integrate real-time processing of images directly from microscopes.
- **Advanced Visualization**: Provide 3D visualization of chromosome arrangements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.