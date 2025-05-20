import React, { createContext, useContext, useReducer } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { StrategyForum, NewStrategy, StrategyDetail } from './pages';
import { Navbar } from './components';
import initialData from './mockData';
import './styles.css';

// Create Data Context
const DataContext = createContext();

// Actions
const ADD_STRATEGY = 'ADD_STRATEGY';
const TOGGLE_LIKE = 'TOGGLE_LIKE';
const ADD_COMMENT = 'ADD_COMMENT';
const TOGGLE_FOLLOW = 'TOGGLE_FOLLOW';

// Reducer
function dataReducer(state, action) {
  switch (action.type) {
    case ADD_STRATEGY:
      return {
        ...state,
        strategies: [action.payload, ...state.strategies]
      };
    case TOGGLE_LIKE:
      return {
        ...state,
        strategies: state.strategies.map(strategy => 
          strategy.id === action.payload
            ? { ...strategy, liked: !strategy.liked, likes: strategy.liked ? strategy.likes - 1 : strategy.likes + 1 }
            : strategy
        )
      };
    case ADD_COMMENT:
      return {
        ...state,
        comments: [...state.comments, action.payload]
      };
    case TOGGLE_FOLLOW:
      return {
        ...state,
        users: state.users.map(user => 
          user.id === action.payload
            ? { ...user, followed: !user.followed }
            : user
        )
      };
    default:
      return state;
  }
}

// App Component
function App() {
  const [data, dispatch] = useReducer(dataReducer, initialData);

  // Actions
  const addStrategy = (strategy) => {
    dispatch({ 
      type: ADD_STRATEGY, 
      payload: { 
        ...strategy,
        id: Date.now().toString(),
        date: new Date().toISOString(),
        likes: 0,
        liked: false,
      } 
    });
  };

  const toggleLike = (strategyId) => {
    dispatch({ type: TOGGLE_LIKE, payload: strategyId });
  };

  const addComment = (comment) => {
    dispatch({ 
      type: ADD_COMMENT, 
      payload: { 
        ...comment,
        id: Date.now().toString(),
        date: new Date().toISOString(),
      } 
    });
  };

  const toggleFollow = (userId) => {
    dispatch({ type: TOGGLE_FOLLOW, payload: userId });
  };

  return (
    <DataContext.Provider value={{ data, addStrategy, toggleLike, addComment, toggleFollow }}>
      <BrowserRouter>
        <div className="app">
          <Navbar />
          <main className="content">
            <Routes>
              <Route path="/" element={
                <StrategyForum 
                  data={data} 
                  toggleLike={toggleLike} 
                  toggleFollow={toggleFollow} 
                />
              } />
              <Route path="/new" element={
                <NewStrategy 
                  addStrategy={addStrategy} 
                />
              } />
              <Route path="/strategy/:id" element={
                <StrategyDetail 
                  data={data} 
                  toggleLike={toggleLike} 
                  addComment={addComment} 
                  toggleFollow={toggleFollow} 
                />
              } />
            </Routes>
          </main>
        </div>
      </BrowserRouter>
    </DataContext.Provider>
  );
}

export default App;
