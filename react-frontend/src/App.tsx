import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

const App: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [resultImage, setResultImage] = useState<string | null>(null);
  const [barChart, setBarChart] = useState<string | null>(null);
  const [disorders, setDisorders] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      setLoading(true);
      setError(null); // Clear any previous errors

      const response = await axios.post('http://127.0.0.1:5000/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const { result_image, bar_chart, disorders } = response.data;

      // Ensure state is set only if valid data is returned
      if (result_image && bar_chart && disorders) {
        setResultImage(result_image);
        setBarChart(bar_chart);
        setDisorders(disorders);
      } else {
        setError('Invalid data received from the server.');
      }
    } catch (error) {
      setError('There was an error uploading the file or processing the request.');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    console.log("Disorders state updated:", disorders); // Watch state changes
  }, [disorders]);

  return (
    <div className="container">
      <aside className="sidebar">
        <section className="about-section">
          <h2>About R.E.B.E.C.C.A</h2>
          <p>
            R.E.B.E.C.C.A (Recognition of Essential Biological Elements in Chromosome Configuration Analysis)
            is an advanced AI designed for chromosome analysis. It utilizes YOLO-based object detection models
            to identify essential biological elements, providing insights into chromosomal disorders.
          </p>
        </section>
        <section className="upload-section">
          <h2>Upload Image</h2>
          <form onSubmit={handleSubmit}>
            <input type="file" accept="image/*" onChange={handleFileChange} required />
            <button type="submit">Upload</button>
          </form>
        </section>
      </aside>

      <main className="content">
        <h1>R.E.B.E.C.C.A</h1>
        <h2>Recognition of Essential Biological Elements in Chromosome Configuration Analysis</h2>
        <h3>கருவில் பிறந்த எல்லாம் மரிக்கும், அறிவில் பிறந்தது மரிப்பதே இல்லை</h3>

        {loading && <p>Processing...</p>}
        {error && <p style={{ color: 'red' }}>{error}</p>}

        {!loading && resultImage && (
          <>
            <h2>Result Image</h2>
            <img src={`http://127.0.0.1:5000/results/${resultImage}`} alt="Result" style={{ maxWidth: '100%', height: 'auto' }} />
          </>
        )}

        {!loading && barChart && (
          <>
            <h2>Category Count Bar Chart</h2>
            <img src={`http://127.0.0.1:5000/results/${barChart}`} alt="Bar Chart" style={{ maxWidth: '100%', height: 'auto' }} />
          </>
        )}

        {!loading && disorders.length > 0 && (
          <>
            <h2>Detected Chromosomal Disorders</h2>
            <ul>
              {disorders.map((disorder, index) => (
                <li key={index}>{disorder}</li>
              ))}
            </ul>
          </>
        )}

        {!loading && resultImage && disorders.length === 0 && (
          <p>No chromosomal disorders detected</p>
        )}
      </main>
    </div>
  );
};

export default App;
