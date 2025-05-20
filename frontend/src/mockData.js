// Mock data for the Strategy Forum application
export const initialData = {
  strategies: [
    {
      id: "1",
      title: "Mean Reversion Strategy for Forex",
      description: "This strategy identifies overbought and oversold conditions in currency pairs. It uses Bollinger Bands and RSI indicators to identify potential reversal points. When price touches the upper Bollinger Band and RSI is above 70, it signals a sell opportunity. Conversely, when price touches the lower Bollinger Band and RSI is below 30, it signals a buy opportunity. The strategy includes proper position sizing (1% risk per trade) and implements a 2:1 reward-to-risk ratio for all trades with proper stop losses.",
      authorId: "1",
      date: "2025-05-15T10:30:00Z",
      likes: 42,
      liked: false,
      visibility: "public"
    },
    {
      id: "2",
      title: "Trend Following Strategy with Moving Averages",
      description: "This strategy focuses on capturing strong market trends using multiple moving averages. It uses a combination of 9 EMA, 21 EMA, and 50 SMA to identify trend direction and potential entry points. When the 9 EMA crosses above the 21 EMA and both are above the 50 SMA, it generates a buy signal. When the 9 EMA crosses below the 21 EMA and both are below the 50 SMA, it generates a sell signal. The strategy performs best in trending markets and includes trailing stops to maximize profits during strong trends.",
      authorId: "2",
      date: "2025-05-14T15:45:00Z",
      likes: 38,
      liked: false,
      visibility: "public"
    },
    {
      id: "3",
      title: "Options Iron Condor for Low Volatility Markets",
      description: "This options strategy capitalizes on low volatility environments using iron condors. By selling both an out-of-the-money call spread and an out-of-the-money put spread with the same expiration date, this strategy profits when the underlying asset stays within a specific price range. The ideal setup is during periods of low implied volatility and no expected major news events. Position sizing is critical, with maximum risk limited to 2% of account per trade.",
      authorId: "3",
      date: "2025-05-13T09:15:00Z",
      likes: 27,
      liked: false,
      visibility: "public"
    },
    {
      id: "4",
      title: "Volatility Breakout for Intraday Trading",
      description: "This intraday strategy captures explosive price movements following tight consolidation periods. It waits for price to compress (measured by decreasing Average True Range) followed by a surge in volume and price movement outside the consolidation range. The strategy works best during the first 2 hours of market open or near significant news events. Entry is triggered when price breaks above/below the consolidation with volume confirmation, with tight stop losses placed just inside the consolidation range.",
      authorId: "1",
      date: "2025-05-12T14:20:00Z",
      likes: 31,
      liked: false,
      visibility: "public"
    }
  ],
  comments: [
    {
      id: "101",
      strategyId: "1",
      authorId: "2",
      text: "I've been testing this strategy for the past month and have seen consistent results. The key is to be patient and wait for clear signals rather than forcing trades.",
      date: "2025-05-16T08:30:00Z",
      parentId: null
    },
    {
      id: "102",
      strategyId: "1",
      authorId: "3",
      text: "Have you tried adjusting the RSI thresholds for different currency pairs? I've found that some pairs work better with custom settings.",
      date: "2025-05-16T10:15:00Z",
      parentId: null
    },
    {
      id: "103",
      strategyId: "1",
      authorId: "1",
      text: "Good point! For EUR/USD I use 75/25 thresholds instead of the standard 70/30.",
      date: "2025-05-16T11:05:00Z",
      parentId: "102"
    },
    {
      id: "104",
      strategyId: "2",
      authorId: "3",
      text: "This works really well in strong trending markets, but be careful during choppy consolidation periods. I add a trend filter using ADX to avoid false signals.",
      date: "2025-05-15T09:45:00Z",
      parentId: null
    },
    {
      id: "105",
      strategyId: "3",
      authorId: "1",
      text: "Great strategy. I recommend calculating position size based on implied volatility too, not just account percentage.",
      date: "2025-05-14T16:20:00Z",
      parentId: null
    }
  ],
  users: [
    {
      id: "1",
      name: "Alex Johnson",
      karma: 387,
      followed: false,
      strategies: ["1", "4"]
    },
    {
      id: "2",
      name: "Maya Rodriguez",
      karma: 259,
      followed: false,
      strategies: ["2"]
    },
    {
      id: "3",
      name: "Tao Chen",
      karma: 412,
      followed: false,
      strategies: ["3"]
    }
  ]
};

export default initialData;
