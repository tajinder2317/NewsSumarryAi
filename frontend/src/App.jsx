import React, { Suspense, lazy } from "react";
import { Routes, Route } from "react-router-dom";
import { Container } from "@mui/material";
import { QueryClientProvider, QueryClient } from "react-query";

import Header from "./components/common/Header";
import Footer from "./components/common/Footer";
import ErrorBoundary from "./components/common/ErrorBoundary";
import Loading from "./components/common/Loading";

const Home = lazy(() => import("./pages/Home"));
const Dashboard = lazy(() => import("./pages/Dashboard"));
const Analysis = lazy(() => import("./pages/Analysis"));
const Search = lazy(() => import("./pages/Search"));
const News = lazy(() => import("./pages/News"));

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="app-container">
        <Header />

        <main className="main-content">
          <Container maxWidth="xl">
            <ErrorBoundary>
              <Suspense fallback={<Loading message="Loading page..." />}>
                <Routes>
                  <Route path="/" element={<Home />} />
                  <Route path="/dashboard" element={<Dashboard />} />
                  <Route path="/analysis" element={<Analysis />} />
                  <Route path="/search" element={<Search />} />
                  <Route path="/news" element={<News />} />
                </Routes>
              </Suspense>
            </ErrorBoundary>
          </Container>
        </main>

        <Footer />
      </div>
    </QueryClientProvider>
  );
}

export default App;
