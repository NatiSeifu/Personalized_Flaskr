import React, { useState } from 'react';

function Post({ id, title, body, author }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(title);
  const [editBody, setEditBody] = useState(body);

  const handleUpdate = () => {
    fetch(`http://localhost:5000/api/posts/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        title: editTitle,
        body: editBody
      }),
    })
      .then(res => {
        if (!res.ok) throw new Error('Update failed');
        return res.json();
      })
      .then(() => {
        setIsEditing(false);
        window.location.reload(); // or better: trigger parent state update
      })
      .catch(err => {
        console.error('Error updating post:', err);
      });
  };

  return (
    <div className="post">
      {isEditing ? (
        <>
          <input
            value={editTitle}
            onChange={e => setEditTitle(e.target.value)}
          />
          <textarea
            value={editBody}
            onChange={e => setEditBody(e.target.value)}
          />
          <button onClick={handleUpdate}>Save</button>
          <button onClick={() => setIsEditing(false)}>Cancel</button>
        </>
      ) : (
        <>
          <h2>{title}</h2>
          <p>{body}</p>
          <small>By {author}</small>
          <button onClick={() => setIsEditing(true)}>Edit</button>
        </>
      )}
    </div>
  );
}

export default Post;

