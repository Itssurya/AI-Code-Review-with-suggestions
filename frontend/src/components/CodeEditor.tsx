import React, { useState, useEffect } from 'react';
import { Play, FileText, Code2, Upload } from 'lucide-react';
import { apiService } from '../services/api';

interface CodeEditorProps {
  onReview: (code: string, language: string, fileName: string) => void;
  isLoading: boolean;
}

const LANGUAGES = [
  { value: 'python', label: 'Python', extension: '.py' },
  { value: 'javascript', label: 'JavaScript', extension: '.js' },
  { value: 'typescript', label: 'TypeScript', extension: '.ts' },
  { value: 'java', label: 'Java', extension: '.java' },
  { value: 'cpp', label: 'C++', extension: '.cpp' },
  { value: 'c', label: 'C', extension: '.c' },
  { value: 'go', label: 'Go', extension: '.go' },
  { value: 'rust', label: 'Rust', extension: '.rs' },
];

const SAMPLE_CODE = {
  python: `def calculate_fibonacci(n):
    """Calculate the nth Fibonacci number."""
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

def main():
    number = int(input("Enter a number: "))
    result = calculate_fibonacci(number)
    print(f"The {number}th Fibonacci number is {result}")

if __name__ == "__main__":
    main()`,
  javascript: `function calculateFibonacci(n) {
    if (n <= 1) return n;
    return calculateFibonacci(n - 1) + calculateFibonacci(n - 2);
}

function main() {
    const number = parseInt(prompt("Enter a number:"));
    const result = calculateFibonacci(number);
    console.log(\`The \${number}th Fibonacci number is \${result}\`);
}

main();`,
  typescript: `function calculateFibonacci(n: number): number {
    if (n <= 1) return n;
    return calculateFibonacci(n - 1) + calculateFibonacci(n - 2);
}

function main(): void {
    const number: number = parseInt(prompt("Enter a number:") || "0");
    const result: number = calculateFibonacci(number);
    console.log(\`The \${number}th Fibonacci number is \${result}\`);
}

main();`,
};

export const CodeEditor: React.FC<CodeEditorProps> = ({ onReview, isLoading }) => {
  const [code, setCode] = useState(SAMPLE_CODE.python);
  const [language, setLanguage] = useState('python');
  const [fileName, setFileName] = useState('example.py');
  const [supportedLanguages, setSupportedLanguages] = useState<string[]>([]);

  useEffect(() => {
    loadSupportedLanguages();
  }, []);

  useEffect(() => {
    const selectedLang = LANGUAGES.find(lang => lang.value === language);
    if (selectedLang) {
      setFileName(`example${selectedLang.extension}`);
      setCode(SAMPLE_CODE[language as keyof typeof SAMPLE_CODE] || SAMPLE_CODE.python);
    }
  }, [language]);

  const loadSupportedLanguages = async () => {
    try {
      const languages = await apiService.getSupportedLanguages();
      setSupportedLanguages(languages);
    } catch (error) {
      console.error('Failed to load supported languages:', error);
      setSupportedLanguages(LANGUAGES.map(lang => lang.value));
    }
  };

  const handleReview = () => {
    if (code.trim()) {
      onReview(code, language, fileName);
    }
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const content = e.target?.result as string;
        setCode(content);
        
        // Try to detect language from file extension
        const extension = file.name.split('.').pop()?.toLowerCase();
        const detectedLang = LANGUAGES.find(lang => 
          lang.extension.substring(1) === extension
        );
        if (detectedLang) {
          setLanguage(detectedLang.value);
          setFileName(file.name);
        }
      };
      reader.readAsText(file);
    }
  };

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-2">
          <Code2 className="w-5 h-5 text-primary-600" />
          <h2 className="text-xl font-bold text-gray-900">Code Editor</h2>
        </div>
        
        <div className="flex items-center space-x-2">
          <label className="btn-secondary cursor-pointer">
            <Upload className="w-4 h-4 mr-2" />
            Upload File
            <input
              type="file"
              accept=".py,.js,.ts,.java,.cpp,.c,.go,.rs"
              onChange={handleFileUpload}
              className="hidden"
            />
          </label>
        </div>
      </div>

      <div className="space-y-4">
        {/* Language and File Name Selection */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Programming Language
            </label>
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="input-field"
            >
              {LANGUAGES.map((lang) => (
                <option key={lang.value} value={lang.value}>
                  {lang.label}
                </option>
              ))}
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              File Name
            </label>
            <input
              type="text"
              value={fileName}
              onChange={(e) => setFileName(e.target.value)}
              className="input-field"
              placeholder="example.py"
            />
          </div>
        </div>

        {/* Code Editor */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Code
          </label>
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            className="code-editor w-full h-96 p-4 resize-none"
            placeholder="Enter your code here..."
            spellCheck={false}
          />
        </div>

        {/* Action Buttons */}
        <div className="flex items-center justify-between">
          <div className="text-sm text-gray-500">
            {code.length} characters, {code.split('\n').length} lines
          </div>
          
          <button
            onClick={handleReview}
            disabled={isLoading || !code.trim()}
            className="btn-primary flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Play className="w-4 h-4" />
            <span>Review Code</span>
          </button>
        </div>
      </div>
    </div>
  );
};

