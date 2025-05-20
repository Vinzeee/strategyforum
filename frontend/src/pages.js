import React, { useState, useEffect } from 'react';
import { useLocation, Link, useParams, useNavigate } from 'react-router-dom';
import { FaHeart, FaRegHeart, FaUser } from 'react-icons/fa';
import { StrategyCard, SearchBar, AuthorFilter, CommentItem, UserProfile } from './components';

// Strategy Forum Page (Homepage)
export function StrategyForum({ data, toggleLike, toggleFollow }) {
  const location = useLocation();
  const navigate = useNavigate();
  
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedAuthor, setSelectedAuthor] = useState(null);
  const [selectedUserId, setSelectedUserId] = useState(null);
  
  // Handle URL params for filtering
  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const authorParam = params.get('author');
    if (authorParam) {
      setSelectedAuthor(authorParam);
    } else {
      setSelectedAuthor(null);
    }
  }, [location]);

  // Filter strategies
  const filteredStrategies = data.strategies.filter(strategy => {
    const authorMatch = selectedAuthor ? strategy.authorId === selectedAuthor : true;
    const searchMatch = searchTerm 
      ? strategy.title.toLowerCase().includes(searchTerm.toLowerCase()) 
      : true;
    return authorMatch && searchMatch && strategy.visibility === 'public';
  });

  // Get author name
  const getAuthorName = (authorId) => {
    const author = data.users.find(user => user.id === authorId);
    return author ? author.name : 'Unknown User';
  };

  return (
    <div className="strategy-forum">
      <div className="forum-header">
        <h1>Trading Strategies</h1>
        <Link to="/new" className="create-strategy-button">
          New Strategy
        </Link>
      </div>
      
      <div className="filters-container">
        <SearchBar 
          searchTerm={searchTerm} 
          setSearchTerm={setSearchTerm} 
        />
        
        {selectedAuthor && (
          <AuthorFilter 
            authorName={getAuthorName(selectedAuthor)}
            clearFilter={() => {
              setSelectedAuthor(null);
              navigate('/');
            }}
          />
        )}
      </div>
      
      <div className="strategies-list">
        {filteredStrategies.length > 0 ? (
          filteredStrategies.map(strategy => {
            const author = data.users.find(u => u.id === strategy.authorId);
            const commentCount = data.comments.filter(c => c.strategyId === strategy.id).length;
            
            return (
              <StrategyCard 
                key={strategy.id} 
                strategy={strategy} 
                author={author}
                commentCount={commentCount}
                toggleLike={toggleLike}
              />
            );
          })
        ) : (
          <div className="no-strategies">
            <p>No strategies found. Try adjusting your filters.</p>
          </div>
        )}
      </div>
      
      {selectedUserId && (
        <div className="user-profile-overlay">
          <div className="user-profile-container">
            <UserProfile 
              user={data.users.find(u => u.id === selectedUserId)}
              userStrategies={data.strategies.filter(s => s.authorId === selectedUserId)}
              toggleFollow={toggleFollow}
              onClose={() => setSelectedUserId(null)} 
            />
          </div>
        </div>
      )}
    </div>
  );
}

// New Strategy Form Page
export function NewStrategy({ addStrategy }) {
  const navigate = useNavigate();
  
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [visibility, setVisibility] = useState('public');
  const [errors, setErrors] = useState({});

  const validateForm = () => {
    const newErrors = {};
    if (!title.trim()) newErrors.title = 'Title is required';
    if (!description.trim()) newErrors.description = 'Description is required';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (validateForm()) {
      // Mock user ID (in a real app, this would come from auth)
      const currentUserId = "1"; 
      
      addStrategy({
        title,
        description,
        authorId: currentUserId,
        visibility
      });
      
      // Redirect to home page
      navigate('/');
    }
  };

  return (
    <div className="new-strategy-page">
      <h1>Create New Strategy</h1>
      
      <form className="strategy-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="title">Title</label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className={errors.title ? 'error' : ''}
          />
          {errors.title && <span className="error-text">{errors.title}</span>}
        </div>
        
        <div className="form-group">
          <label htmlFor="description">Description</label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows="8"
            className={errors.description ? 'error' : ''}
          />
          {errors.description && <span className="error-text">{errors.description}</span>}
        </div>
        
        <div className="form-group">
          <label htmlFor="visibility">Visibility</label>
          <select
            id="visibility"
            value={visibility}
            onChange={(e) => setVisibility(e.target.value)}
          >
            <option value="public">Public</option>
            <option value="private">Private</option>
          </select>
        </div>
        
        <div className="form-actions">
          <button 
            type="button" 
            className="cancel-button"
            onClick={() => navigate('/')}
          >
            Cancel
          </button>
          <button type="submit" className="submit-button">
            Post Strategy
          </button>
        </div>
      </form>
    </div>
  );
}

// Strategy Detail Page
export function StrategyDetail({ data, toggleLike, addComment, toggleFollow }) {
  const { id } = useParams();
  const navigate = useNavigate();
  
  const [comment, setComment] = useState('');
  const [showUserProfile, setShowUserProfile] = useState(false);
  
  const strategy = data.strategies.find(s => s.id === id);
  if (!strategy) {
    return (
      <div className="strategy-not-found">
        <h2>Strategy Not Found</h2>
        <p>The strategy you're looking for doesn't exist or has been removed.</p>
        <Link to="/">Return to Forum</Link>
      </div>
    );
  }
  
  const author = data.users.find(user => user.id === strategy.authorId);
  const comments = data.comments
    .filter(c => c.strategyId === id && c.parentId === null)
    .sort((a, b) => new Date(b.date) - new Date(a.date));
  
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric',
      month: 'long', 
      day: 'numeric'
    });
  };
  
  const handleSubmitComment = (e) => {
    e.preventDefault();
    if (!comment.trim()) return;
    
    // Mock user ID (in a real app, this would come from auth)
    const currentUserId = "1";
    
    addComment({
      strategyId: id,
      authorId: currentUserId,
      text: comment,
      parentId: null
    });
    
    setComment('');
  };
  
  return (
    <div className="strategy-detail-page">
      <div className="strategy-navigation">
        <Link to="/" className="back-link">← Back to Forum</Link>
      </div>
      
      <div className="strategy-header">
        <h1>{strategy.title}</h1>
        <div className="strategy-meta">
          <div 
            className="author-info"
            onClick={() => setShowUserProfile(true)}
          >
            <FaUser />
            <span>{author ? author.name : 'Unknown User'}</span>
          </div>
          <div className="date-info">
            {formatDate(strategy.date)}
          </div>
        </div>
      </div>
      
      <div className="strategy-content">
        <p>{strategy.description}</p>
      </div>
      
      <div className="strategy-actions">
        <button 
          className={`like-button ${strategy.liked ? 'liked' : ''}`}
          onClick={() => toggleLike(strategy.id)}
        >
          {strategy.liked ? <FaHeart /> : <FaRegHeart />}
          <span>{strategy.likes}</span>
        </button>
      </div>
      
      <div className="strategy-metrics">
        <h3>Strategy Metrics</h3>
        <div className="metrics-grid">
          <div className="metric">
            <div className="metric-label">Win Rate</div>
            <div className="metric-value">68%</div>
          </div>
          <div className="metric">
            <div className="metric-label">Risk-Reward</div>
            <div className="metric-value">1:2.5</div>
          </div>
          <div className="metric">
            <div className="metric-label">Max Drawdown</div>
            <div className="metric-value">12.4%</div>
          </div>
          <div className="metric">
            <div className="metric-label">Sharpe Ratio</div>
            <div className="metric-value">1.8</div>
          </div>
        </div>
      </div>
      
      <div className="comments-section">
        <h3>Comments ({comments.length})</h3>
        
        <form className="comment-form" onSubmit={handleSubmitComment}>
          <textarea
            placeholder="Add a comment..."
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            rows="3"
          />
          <button type="submit" disabled={!comment.trim()}>
            Post Comment
          </button>
        </form>
        
        <div className="comments-list">
          {comments.length > 0 ? (
            comments.map(comment => {
              const commentAuthor = data.users.find(u => u.id === comment.authorId);
              const childComments = data.comments.filter(c => c.parentId === comment.id);
              
              return (
                <CommentItem 
                  key={comment.id} 
                  comment={comment}
                  author={commentAuthor}
                  childComments={childComments}
                  allComments={data}
                />
              );
            })
          ) : (
            <p className="no-comments">No comments yet. Be the first to comment!</p>
          )}
        </div>
      </div>
      
      {showUserProfile && (
        <div className="user-profile-overlay">
          <div className="user-profile-container">
            <UserProfile 
              user={author} 
              userStrategies={data.strategies.filter(s => s.authorId === author.id)}
              toggleFollow={toggleFollow}
              onClose={() => setShowUserProfile(false)} 
            />
          </div>
        </div>
      )}
    </div>
  );
}
