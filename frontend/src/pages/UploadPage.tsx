import React, { useState } from 'react';
import axios from 'axios';
import '../styles/UploadPage.css';

interface FileInfo {
  filename: string;
  file_id: string;
  size: number;
}

const UploadPage: React.FC = () => {
  const [dragActive, setDragActive] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<FileInfo | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [translating, setTranslating] = useState(false);
  const [translatedText, setTranslatedText] = useState<string | null>(null);

  const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

  const handleDrag = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0];
      if (droppedFile.type === 'application/pdf') {
        setFile(droppedFile);
        setError(null);
      } else {
        setError('Please drop a PDF file');
      }
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setUploading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/api/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setUploadedFile(response.data);
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Upload failed');
      setUploadedFile(null);
    } finally {
      setUploading(false);
    }
  };

  const handleTranslate = async () => {
    if (!uploadedFile) {
      setError('Please upload a file first');
      return;
    }

    setTranslating(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/api/translate`, {
        filename: uploadedFile.filename,
        target_language: 'Japanese',
        preserve_formatting: true,
      });
      setTranslatedText(response.data.translated_text);
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Translation failed');
    } finally {
      setTranslating(false);
    }
  };

  return (
    <div className="upload-container">
      <div className="upload-card">
        <h2>Upload Chemistry Paper</h2>

        {!uploadedFile ? (
          <>
            <div
              className={`drag-drop-area ${dragActive ? 'active' : ''}`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              <input
                type="file"
                accept=".pdf"
                onChange={handleFileChange}
                className="file-input"
                id="file-input"
              />
              <label htmlFor="file-input" className="file-label">
                <div className="upload-icon">📄</div>
                <p>Drag and drop your PDF here</p>
                <p className="small-text">or click to select</p>
              </label>
            </div>

            {file && (
              <div className="file-info">
                <p><strong>Selected:</strong> {file.name}</p>
                <p><strong>Size:</strong> {(file.size / 1024 / 1024).toFixed(2)} MB</p>
              </div>
            )}

            {error && <div className="error-message">{error}</div>}

            <button
              className="upload-button"
              onClick={handleUpload}
              disabled={!file || uploading}
            >
              {uploading ? 'Uploading...' : 'Upload PDF'}
            </button>
          </>
        ) : (
          <>
            <div className="success-message">
              <p>✓ File uploaded successfully!</p>
              <p><strong>{uploadedFile.filename}</strong></p>
            </div>

            {!translatedText ? (
              <button
                className="translate-button"
                onClick={handleTranslate}
                disabled={translating}
              >
                {translating ? 'Translating...' : 'Translate to Japanese'}
              </button>
            ) : (
              <div className="translation-result">
                <h3>Translation Result</h3>
                <div className="translated-text">
                  {translatedText.substring(0, 500)}...
                </div>
                <button
                  className="reset-button"
                  onClick={() => {
                    setFile(null);
                    setUploadedFile(null);
                    setTranslatedText(null);
                  }}
                >
                  Translate Another Paper
                </button>
              </div>
            )}

            {error && <div className="error-message">{error}</div>}
          </>
        )}
      </div>
    </div>
  );
};

export default UploadPage;
