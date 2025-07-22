import React from 'react';
import './Post.css';

function Post({ title, body, author }) {
  return (
    <div className="post">
      <h2 className="post-title">{title}</h2>
      <p className="post-body">{body}</p>
      <small className="post-author">By {author}</small>
    </div>
  );
}

export default Post; 