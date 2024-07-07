"use client";

import React, { useState } from 'react';
import classNames from 'classnames';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm'
import Skeleton from 'react-loading-skeleton';
import 'react-loading-skeleton/dist/skeleton.css';


export default function Page() {

  const [isFirstQuestion, setIsFirstQuestion] = useState(true);
  const [submittedText, setSubmittedText] = useState('');
  const [inputText, setInputText] = useState("");
  const [chatHistory, setChatHistory] = useState("");
  const [loading, setLoading] = useState(false);

  function submissionHandler() {
    const userText: string = inputText;
    setSubmittedText(inputText);
    setIsFirstQuestion(false);
    setInputText("");
    fetchData(userText);
  }

  async function fetchData(userText: String) {
    setLoading(true);
    try {
      const response = await fetch(process.env.NEXT_PUBLIC_API_URL + 'search?q=' + userText); 
      if (!response.ok) {
        throw new Error('Network response was not ok ' + response.statusText);
      }
      setChatHistory(await response.text())
      //setChatHistory("## Text")
    }
    catch (error) {
      console.error('There was a problem with the fetch operation:', error);
    }   
    finally {
      setLoading(false);
    }
  } 

  return (
    <div className="flex flex-col min-h-screen">
      <h1 className = 'text-4xl text-center py-6'> {submittedText} </h1>
      {!isFirstQuestion && (
        <div className="flex-grow overflow-auto pb-24">
          <div className = 'max-w-3xl mx-auto'>
            <div className = 'text-left font-semibold text-lg mb-2'>Answer: </div>
            {!loading ? <ReactMarkdown remarkPlugins={[remarkGfm]} className="prose prose-sm sm:prose">
              {chatHistory}
            </ReactMarkdown> :
            <><Skeleton height={30} width={200} />
            <Skeleton height={20} count={3} /></>}            
          </div>
        </div>
      )}
  
    <div className={classNames(
      'bg-white p-4 flex justify-center',
      isFirstQuestion ? 'flex-grow flex items-center' : 'sticky bottom-0'
    )}>
        <div className="w-full max-w-3xl flex">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Ask any question here..."
            className="flex-grow p-3 text-lg border border-gray-300 rounded-l-lg shadow-md"
          />
          <button 
            className="w-16 text-lg text-white bg-blue-500 rounded-r-lg shadow-md hover:bg-blue-600 flex items-center justify-center"
            onClick={submissionHandler}
          >
            ↑
          </button>
        </div>
      </div>
    </div>
  );
}