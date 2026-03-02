import { useState, useRef } from 'react'
import './App.css'

function App() {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const fileInputRef = useRef(null)

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      setFile(selectedFile)
      setPreview(URL.createObjectURL(selectedFile))
      setResult(null)
      setError(null)
    }
  }

  const handleScan = async () => {
    if (!file) return

    setLoading(true)
    setError(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('/api/predict', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Prediction failed')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    const droppedFile = e.dataTransfer.files[0]
    if (droppedFile) {
      setFile(droppedFile)
      setPreview(URL.createObjectURL(droppedFile))
      setResult(null)
      setError(null)
    }
  }

  return (
    <div className="container">
      <header>
        <h1>MemeModerator AI</h1>
        <p className="subtitle">Advanced multimodal hateful content detection</p>
      </header>

      <main className="main-card">
        <div className="upload-section">
          <div
            className={`dropzone ${file ? 'active' : ''}`}
            onDragOver={(e) => e.preventDefault()}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current.click()}
          >
            <span className="upload-icon">🖼️</span>
            <p>{file ? file.name : 'Drag & drop meme or click to browse'}</p>
            <input
              type="file"
              className="file-input"
              ref={fileInputRef}
              onChange={handleFileChange}
              accept="image/*"
            />
          </div>

          {preview && (
            <div className="preview-container">
              <img src={preview} alt="Preview" className="preview-img" />
            </div>
          )}

          <button
            className="btn-scan"
            onClick={handleScan}
            disabled={!file || loading}
          >
            {loading ? (
              <div className="loading">
                <div className="spinner"></div>
                Analyzing Content...
              </div>
            ) : 'Analyze Meme'}
          </button>

          {error && <p style={{ color: '#ef4444', textAlign: 'center' }}>{error}</p>}
        </div>

        <div className={`results-section ${result || loading ? 'visible' : ''}`}>
          {!result && !loading && (
            <div className="loading" style={{ opacity: 0.5 }}>
              Waiting for analysis...
            </div>
          )}

          {loading && (
            <div className="loading">
              <div className="spinner"></div>
              <span>Neural networks processing...</span>
            </div>
          )}

          {result && (
            <>
              <div>
                <span className={`result-badge ${result.classification === 'HATEFUL' ? 'badge-hate' : 'badge-safe'}`}>
                  {result.classification === 'HATEFUL' ? '🚫 Hateful Content' : '✅ Safe Content'}
                </span>
              </div>

              <div className="score-container">
                <div className="score-header">
                  <span className="score-label">Confidence Score</span>
                  <span className="score-value">{(result.confidence * 100).toFixed(1)}%</span>
                </div>
                <div className="progress-bar-bg">
                  <div
                    className="progress-bar-fill"
                    style={{
                      width: `${result.confidence * 100}%`,
                      backgroundColor: result.classification === 'HATEFUL' ? 'var(--accent-hate)' : 'var(--accent-safe)'
                    }}
                  ></div>
                </div>
              </div>

              <div className="ocr-box">
                <span className="ocr-title">EXTRACTED TEXT</span>
                <p className="ocr-content">
                  {result.extracted_text || 'No text detected in image.'}
                </p>
              </div>
            </>
          )}
        </div>
      </main>
    </div>
  )
}

export default App
