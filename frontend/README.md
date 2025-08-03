# Streamlit Frontend for Sentiment Analysis

This is the frontend application that provides an interactive web interface for the sentiment analysis service.

## 🚀 Features

- **Interactive Web Interface**: Beautiful, responsive Streamlit application
- **Real-time Analysis**: Instant sentiment predictions with confidence scores
- **Batch Processing**: Analyze multiple texts simultaneously
- **File Upload Support**: Upload text files for batch analysis
- **Visual Feedback**: Progress bars, confidence indicators, and color coding
- **Example Gallery**: Pre-loaded examples for quick testing
- **API Health Monitoring**: Real-time backend status checking
- **Mobile Responsive**: Works on desktop, tablet, and mobile devices

## 📁 Structure

```
frontend/
├── app.py                  # Main Streamlit application
├── start.sh               # Startup script (Docker entrypoint)
├── requirements.txt       # Python dependencies
├── docker/
│   └── Dockerfile         # Docker configuration
└── README.md             # This file
```

## 🛠️ Installation & Setup

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the application:**
   ```bash
   streamlit run app.py
   # Or use the startup script
   ./start.sh
   ```

### Docker Deployment

```bash
# Build the image
docker build -f docker/Dockerfile -t sentiment-frontend .

# Run the container
docker run -p 8501:8501 sentiment-frontend
```

## 🎯 Usage Guide

### Single Text Analysis
1. Navigate to the "🔍 Single Prediction" tab
2. Enter your text in the text area
3. Click "🚀 Analyze Sentiment"
4. View results with confidence scores and visual indicators

### Batch Analysis
1. Go to the "📊 Batch Analysis" tab
2. Either:
   - Upload a text file (one text per line)
   - Manually enter multiple texts (one per line)
3. Click "🔍 Analyze All"
4. Review individual results and summary statistics

### Example Testing
1. Visit the "🧪 Examples" tab
2. Click "Analyze" on any pre-loaded example
3. See instant results for testing purposes

## 🔧 Configuration

### API Connection
Update the backend API URL in `app.py`:

```python
# For Docker deployment
API_BASE_URL = "http://backend:8000"

# For local development
API_BASE_URL = "http://localhost:8000"
```

### Streamlit Configuration
The app uses these Streamlit configurations:
- **Page Title**: "Sentiment Analysis App"
- **Page Icon**: 🎭
- **Layout**: Wide
- **Sidebar**: Expanded by default

## 🎨 UI Components

### Main Features
- **Tabbed Interface**: Organized functionality across multiple tabs
- **Sidebar**: API status and application information
- **Progress Indicators**: Visual feedback during processing
- **Metrics Display**: Confidence scores and statistics
- **Color Coding**: Green for positive, red for negative sentiment

### Interactive Elements
- **Text Areas**: For single and batch text input
- **File Upload**: Support for .txt files
- **Buttons**: Primary and secondary action buttons
- **Expandable Sections**: Detailed results in collapsible containers
- **Progress Bars**: Visual confidence representation

## 📊 Features Overview

### Single Prediction Tab
- Large text area for input
- Real-time sentiment analysis
- Confidence percentage display
- Color-coded results
- Input text echo for reference

### Batch Analysis Tab
- File upload functionality
- Manual text input option
- Summary statistics (total, positive, negative counts)
- Individual result details
- Expandable result containers

### Examples Tab
- 8 pre-loaded example texts
- One-click analysis
- Quick result preview
- Testing different sentiment types

### Sidebar Information
- Real-time API health status
- Application description
- Feature overview
- Status indicators

## 🚨 Error Handling

The application handles various error scenarios:

### API Connection Issues
- **Timeout Errors**: 10-second timeout for predictions
- **Connection Refused**: Clear error messages when backend is down
- **Network Issues**: Graceful degradation with user feedback

### Input Validation
- **Empty Text**: Warning messages for empty inputs
- **File Format**: Validation for uploaded files
- **Text Length**: Handling of very long texts

### User Feedback
- **Success Messages**: Green alerts for successful operations
- **Warning Messages**: Yellow alerts for minor issues
- **Error Messages**: Red alerts for serious problems
- **Info Messages**: Blue alerts for general information

## 🎯 User Experience Features

### Visual Design
- **Clean Layout**: Minimalist, professional design
- **Consistent Theming**: Streamlit's default theme with custom colors
- **Responsive Design**: Works on all screen sizes
- **Intuitive Navigation**: Clear tab structure and labels

### Performance
- **Fast Loading**: Lightweight application with quick startup
- **Responsive UI**: Immediate feedback for user actions
- **Efficient API Calls**: Optimized request handling
- **Caching**: Streamlit's built-in caching for better performance

### Accessibility
- **Clear Labels**: Descriptive text for all interactive elements
- **Color Contrast**: Good contrast ratios for readability
- **Keyboard Navigation**: Standard web accessibility features
- **Screen Reader Friendly**: Semantic HTML structure

## 📱 Mobile Support

The application is optimized for mobile devices:
- **Responsive Layout**: Adapts to different screen sizes
- **Touch-Friendly**: Large buttons and touch targets
- **Mobile Navigation**: Streamlined interface for mobile
- **Fast Loading**: Optimized for mobile networks

## 🔍 Advanced Features

### API Health Monitoring
- **Real-time Status**: Continuous health checking
- **Visual Indicators**: Green/red status in sidebar
- **Automatic Retries**: Resilient to temporary API issues
- **Error Recovery**: Graceful handling of API downtime

### Batch Processing Capabilities
- **File Upload**: Support for large text files
- **Progress Tracking**: Visual progress during batch processing
- **Result Export**: Easy copying of batch results
- **Memory Efficient**: Streaming processing for large files

### Result Visualization
- **Confidence Meters**: Progress bars for confidence scores
- **Color Coding**: Intuitive sentiment representation
- **Statistical Summary**: Overview of batch analysis results
- **Detailed Breakdown**: Individual result inspection

## 🧪 Testing

### Manual Testing
1. Test all tabs and features
2. Try different text lengths and types
3. Upload various file formats
4. Test with API offline/online scenarios

### Automated Testing
```bash
# Run from the parent directory to test API integration
python ../test_api.py
```

## 🚨 Troubleshooting

### Common Issues
- **API Not Found**: Ensure backend is running on correct port
- **Slow Loading**: Check network connection and API response times
- **File Upload Errors**: Verify file format and encoding
- **Display Issues**: Try refreshing the browser or clearing cache

### Debug Mode
Enable Streamlit debug mode for development:
```bash
streamlit run app.py --logger.level debug
```

## 📈 Performance Optimization

### Best Practices
- **Efficient API Calls**: Minimize unnecessary requests
- **Caching**: Use Streamlit's caching for repeated operations
- **Lazy Loading**: Load components only when needed
- **Error Boundaries**: Prevent crashes from propagating

### Memory Management
- **Text Limits**: Reasonable limits on input text length
- **Batch Size**: Optimal batch sizes for processing
- **Resource Cleanup**: Proper cleanup of temporary files

## 🔒 Security Considerations

### Input Validation
- **Text Sanitization**: Basic input cleaning
- **File Type Validation**: Restrict to safe file types
- **Size Limits**: Prevent oversized uploads
- **Content Filtering**: Basic content validation

### API Security
- **Request Validation**: Proper request formatting
- **Error Handling**: No sensitive information in error messages
- **Rate Limiting**: Respect API rate limits
- **Timeout Management**: Prevent hanging requests

## 🎨 Customization

### Styling
Customize the appearance by modifying:
- Colors and themes in the Streamlit configuration
- Custom CSS in the app (if needed)
- Layout arrangements and component sizing

### Features
Extend functionality by adding:
- Additional analysis metrics
- Export functionality
- User authentication
- History tracking

## 🤝 Contributing

1. Follow Streamlit best practices
2. Maintain responsive design principles
3. Test across different browsers and devices
4. Update documentation for new features
5. Consider accessibility in all changes
