import React from 'react';
import { Link } from 'react-router-dom';
import { FaHeart, FaRegHeart, FaComment, FaUser, FaChartLine, FaStar, FaSearch } from 'react-icons/fa';

// Navbar Component
export function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <Link to="/">Knead Strategy Forum</Link>
      </div>
      <div className="navbar-links">
        <Link to="/" className="nav-link">Home</Link>
        <Link to="/new" className="nav-link primary-button">New Strategy</Link>
      </div>
    </nav>
  );
}

// Strategy Card Component
export function StrategyCard({ strategy, author, commentCount, toggleLike }) {
  // Format date
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric',
      year: 'numeric' 
    });
  };

  // Get description preview
  const getDescriptionPreview = (description) => {
    return description.length > 150 
      ? description.substring(0, 150) + '...' 
      : description;
  };

  return (
    <div className="strategy-card">
      <Link to={`/strategy/${strategy.id}`} className="strategy-title">
        <h2>{strategy.title}</h2>
      </Link>
      <div className="strategy-meta">
        <span className="strategy-author" onClick={e => e.stopPropagation()}>
          By <Link to={`/?author=${author.id}`}>{author.name}</Link>
        </span>
        <span className="strategy-date">{formatDate(strategy.date)}</span>
      </div>
      <p className="strategy-description-preview">
        {getDescriptionPreview(strategy.description)}
      </p>
      <div className="strategy-actions">
        <div 
          className="like-button"
          onClick={(e) => {
            e.preventDefault();
            toggleLike(strategy.id);
          }}
        >
          {strategy.liked ? <FaHeart color="#ff4757" /> : <FaRegHeart />}
          <span>{strategy.likes}</span>
        </div>
        <div className="comment-count">
          <FaComment />
          <span>{commentCount}</span>
        </div>
      </div>
    </div>
  );
}

// Comment Item Component
export function CommentItem({ comment, author, childComments, allComments }) {
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric',
      hour: '2-digit', 
      minute: '2-digit'
    });
  };

  return (
    <div className="comment-item">
      <div className="comment-header">
        <Link to={`/?author=${author.id}`} className="comment-author">
          {author.name}
        </Link>
        <span className="comment-date">{formatDate(comment.date)}</span>
      </div>
      <div className="comment-content">
        {comment.text}
      </div>
      {childComments && childComments.length > 0 && (
        <div className="comment-replies">
          {childComments.map(childComment => {
            const childAuthor = allComments.users.find(u => u.id === childComment.authorId);
            const grandChildren = allComments.comments.filter(c => c.parentId === childComment.id);
            return (
              <CommentItem 
                key={childComment.id} 
                comment={childComment} 
                author={childAuthor}
                childComments={grandChildren}
                allComments={allComments}
              />
            );
          })}
        </div>
      )}
    </div>
  );
}

// User Profile Component
export function UserProfile({ user, userStrategies, toggleFollow, onClose }) {
  if (!user) return null;

  return (
    <div className="user-profile">
      <div className="profile-header">
        <div className="profile-icon">
          <FaUser size={24} />
        </div>
        <h2>{user.name}</h2>
        <button 
          className={`follow-button ${user.followed ? 'following' : ''}`}
          onClick={() => toggleFollow(user.id)}
        >
          {user.followed ? 'Following' : 'Follow'}
        </button>
        <button className="close-button" onClick={onClose}>×</button>
      </div>
      
      <div className="profile-stats">
        <div className="stat-item">
          <FaStar />
          <span className="stat-label">Karma</span>
          <span className="stat-value">{user.karma}</span>
        </div>
        <div className="stat-item">
          <FaChartLine />
          <span className="stat-label">Strategies</span>
          <span className="stat-value">{userStrategies.length}</span>
        </div>
      </div>
      
      <div className="user-strategies">
        <h3>Recent Strategies</h3>
        <ul>
          {userStrategies.map(strategy => (
            <li key={strategy.id}>
              <Link to={`/strategy/${strategy.id}`} onClick={onClose}>
                {strategy.title}
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

// Search Bar Component
export function SearchBar({ searchTerm, setSearchTerm }) {
  return (
    <div className="search-container">
      <FaSearch />
      <input
        type="text"
        placeholder="Search strategies..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className="search-input"
      />
    </div>
  );
}

// Author Filter Component
export function AuthorFilter({ authorName, clearFilter }) {
  return (
    <div className="author-filter">
      Showing strategies by {authorName}
      <button onClick={clearFilter}>
        Clear Filter
      </button>
    </div>
  );
}
