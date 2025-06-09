#!/usr/bin/env python3
"""
RILEY GENESIS - Web Intelligence Module
Real-time web search, summarization, and knowledge acquisition
"""

import asyncio
import aiohttp
import json
import logging
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from urllib.parse import quote_plus
import re

logger = logging.getLogger(__name__)

@dataclass
class SearchResult:
    """Structure for web search results"""
    title: str
    url: str
    snippet: str
    relevance_score: float
    timestamp: float

@dataclass
class WebSummary:
    """Structure for web content summaries"""
    topic: str
    summary: str
    key_points: List[str]
    sources: List[str]
    confidence: float
    timestamp: float

class WebIntelligence:
    """
    Advanced web intelligence system for RILEY
    
    Features:
    - Real-time web search
    - Content summarization
    - Knowledge extraction
    - Source verification
    - Trend analysis
    """
    
    def __init__(self):
        self.search_engines = {
            "duckduckgo": "https://api.duckduckgo.com/",
            "bing": "https://api.bing.microsoft.com/v7.0/search",
            "google": "https://www.googleapis.com/customsearch/v1"
        }
        
        self.session = None
        self.cache = {}
        self.cache_duration = 3600  # 1 hour
        
        # API keys (set via environment variables)
        self.bing_api_key = None  # os.environ.get("BING_API_KEY")
        self.google_api_key = None  # os.environ.get("GOOGLE_API_KEY")
        self.google_cx = None  # os.environ.get("GOOGLE_CX")
        
        logger.info("🌐 Web Intelligence module initialized")
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    def _is_cache_valid(self, query: str) -> bool:
        """Check if cached result is still valid"""
        if query in self.cache:
            return time.time() - self.cache[query]["timestamp"] < self.cache_duration
        return False
    
    async def search_web(self, query: str, max_results: int = 5) -> List[SearchResult]:
        """
        Perform intelligent web search across multiple engines
        """
        if self._is_cache_valid(query):
            logger.info(f"🔍 Returning cached results for: {query}")
            return self.cache[query]["results"]
        
        results = []
        
        try:
            # Try DuckDuckGo first (no API key required)
            ddg_results = await self._search_duckduckgo(query, max_results)
            results.extend(ddg_results)
            
            # If we have API keys, try other engines
            if self.bing_api_key:
                bing_results = await self._search_bing(query, max_results)
                results.extend(bing_results)
            
            if self.google_api_key and self.google_cx:
                google_results = await self._search_google(query, max_results)
                results.extend(google_results)
            
            # Remove duplicates and sort by relevance
            unique_results = self._deduplicate_results(results)
            sorted_results = sorted(unique_results, key=lambda x: x.relevance_score, reverse=True)
            final_results = sorted_results[:max_results]
            
            # Cache results
            self.cache[query] = {
                "results": final_results,
                "timestamp": time.time()
            }
            
            logger.info(f"🔍 Found {len(final_results)} results for: {query}")
            return final_results
            
        except Exception as e:
            logger.error(f"Web search failed: {e}")
            return []
    
    async def _search_duckduckgo(self, query: str, max_results: int) -> List[SearchResult]:
        """Search using DuckDuckGo Instant Answer API"""
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            # DuckDuckGo Instant Answer API
            url = f"https://api.duckduckgo.com/?q={quote_plus(query)}&format=json&no_html=1&skip_disambig=1"
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    results = []
                    
                    # Process abstract
                    if data.get("Abstract"):
                        results.append(SearchResult(
                            title=data.get("AbstractSource", "DuckDuckGo"),
                            url=data.get("AbstractURL", ""),
                            snippet=data.get("Abstract", ""),
                            relevance_score=0.9,
                            timestamp=time.time()
                        ))
                    
                    # Process related topics
                    for topic in data.get("RelatedTopics", [])[:max_results-1]:
                        if isinstance(topic, dict) and "Text" in topic:
                            results.append(SearchResult(
                                title=topic.get("Text", "")[:50] + "...",
                                url=topic.get("FirstURL", ""),
                                snippet=topic.get("Text", ""),
                                relevance_score=0.7,
                                timestamp=time.time()
                            ))
                    
                    return results
                    
        except Exception as e:
            logger.warning(f"DuckDuckGo search failed: {e}")
        
        return []
    
    async def _search_bing(self, query: str, max_results: int) -> List[SearchResult]:
        """Search using Bing Search API"""
        if not self.bing_api_key:
            return []
        
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            headers = {"Ocp-Apim-Subscription-Key": self.bing_api_key}
            params = {"q": query, "count": max_results, "mkt": "en-US"}
            
            async with self.session.get(self.search_engines["bing"], 
                                      headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    results = []
                    
                    for item in data.get("webPages", {}).get("value", []):
                        results.append(SearchResult(
                            title=item.get("name", ""),
                            url=item.get("url", ""),
                            snippet=item.get("snippet", ""),
                            relevance_score=0.8,
                            timestamp=time.time()
                        ))
                    
                    return results
                    
        except Exception as e:
            logger.warning(f"Bing search failed: {e}")
        
        return []
    
    async def _search_google(self, query: str, max_results: int) -> List[SearchResult]:
        """Search using Google Custom Search API"""
        if not self.google_api_key or not self.google_cx:
            return []
        
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            params = {
                "key": self.google_api_key,
                "cx": self.google_cx,
                "q": query,
                "num": max_results
            }
            
            async with self.session.get(self.search_engines["google"], 
                                      params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    results = []
                    
                    for item in data.get("items", []):
                        results.append(SearchResult(
                            title=item.get("title", ""),
                            url=item.get("link", ""),
                            snippet=item.get("snippet", ""),
                            relevance_score=0.85,
                            timestamp=time.time()
                        ))
                    
                    return results
                    
        except Exception as e:
            logger.warning(f"Google search failed: {e}")
        
        return []
    
    def _deduplicate_results(self, results: List[SearchResult]) -> List[SearchResult]:
        """Remove duplicate search results"""
        seen_urls = set()
        unique_results = []
        
        for result in results:
            if result.url not in seen_urls:
                seen_urls.add(result.url)
                unique_results.append(result)
        
        return unique_results
    
    async def summarize_topic(self, topic: str, max_results: int = 5) -> WebSummary:
        """
        Search for a topic and create an intelligent summary
        """
        try:
            # Search for the topic
            search_results = await self.search_web(topic, max_results)
            
            if not search_results:
                return WebSummary(
                    topic=topic,
                    summary="No reliable information found on this topic.",
                    key_points=[],
                    sources=[],
                    confidence=0.0,
                    timestamp=time.time()
                )
            
            # Extract key information
            all_text = " ".join([result.snippet for result in search_results])
            key_points = self._extract_key_points(all_text)
            summary = self._generate_summary(topic, all_text, key_points)
            sources = [result.url for result in search_results if result.url]
            
            # Calculate confidence based on source quality and consistency
            confidence = self._calculate_confidence(search_results, key_points)
            
            web_summary = WebSummary(
                topic=topic,
                summary=summary,
                key_points=key_points,
                sources=sources,
                confidence=confidence,
                timestamp=time.time()
            )
            
            logger.info(f"📊 Generated summary for '{topic}' with {confidence:.2f} confidence")
            return web_summary
            
        except Exception as e:
            logger.error(f"Topic summarization failed: {e}")
            return WebSummary(
                topic=topic,
                summary=f"Error occurred while researching {topic}",
                key_points=[],
                sources=[],
                confidence=0.0,
                timestamp=time.time()
            )
    
    def _extract_key_points(self, text: str) -> List[str]:
        """Extract key points from text using pattern matching"""
        # Simple key point extraction (can be enhanced with NLP)
        sentences = re.split(r'[.!?]+', text)
        key_points = []
        
        # Look for sentences with important keywords
        important_patterns = [
            r'\b(important|significant|key|main|primary|essential)\b',
            r'\b(discovered|found|research|study|shows)\b',
            r'\b(because|due to|caused by|results in)\b',
            r'\b(however|but|although|despite)\b'
        ]
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20 and len(sentence) < 200:
                for pattern in important_patterns:
                    if re.search(pattern, sentence, re.IGNORECASE):
                        key_points.append(sentence)
                        break
        
        return key_points[:5]  # Return top 5 key points
    
    def _generate_summary(self, topic: str, text: str, key_points: List[str]) -> str:
        """Generate a concise summary from the gathered information"""
        # Simple summarization (can be enhanced with advanced NLP)
        summary_parts = []
        
        # Add topic introduction
        summary_parts.append(f"Based on current web research, {topic} is")
        
        # Add key insights
        if key_points:
            first_point = key_points[0].strip()
            if first_point:
                summary_parts.append(first_point.lower())
        
        # Add additional context if available
        if len(key_points) > 1:
            summary_parts.append(f"Additionally, research indicates that {key_points[1].strip().lower()}")
        
        summary = " ".join(summary_parts)
        
        # Ensure summary is not too long
        if len(summary) > 500:
            summary = summary[:497] + "..."
        
        return summary
    
    def _calculate_confidence(self, results: List[SearchResult], key_points: List[str]) -> float:
        """Calculate confidence score based on result quality"""
        if not results:
            return 0.0
        
        # Base confidence on number of sources
        source_score = min(len(results) / 5.0, 1.0)
        
        # Boost confidence if we have key points
        content_score = min(len(key_points) / 3.0, 1.0)
        
        # Average relevance score
        avg_relevance = sum(r.relevance_score for r in results) / len(results)
        
        # Combined confidence
        confidence = (source_score * 0.3 + content_score * 0.3 + avg_relevance * 0.4)
        
        return min(confidence, 1.0)

# Async wrapper for easy integration
async def search_and_summarize(topic: str, max_results: int = 5) -> WebSummary:
    """Convenience function for searching and summarizing a topic"""
    async with WebIntelligence() as web_intel:
        return await web_intel.summarize_topic(topic, max_results)
