import React from 'react';
import Post from './components/Post'

function App() {
  const samplePost = {
    title: "Hello World",
    body: "This is my first post!",
    author: "Nati"
  };

  return (
    <div>
      <h1>Blog</h1>
      <Post title={samplePost.title} body={samplePost.body} author={samplePost.author} />
    </div>
  );
}

export default App;
