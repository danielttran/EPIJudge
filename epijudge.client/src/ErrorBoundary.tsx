import React, { Component, type ErrorInfo, type ReactNode } from 'react';

type Props = {
  children: ReactNode;
  fallback?: (error: Error, reset: () => void) => ReactNode;
};

type State = {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
};

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error, errorInfo: null };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Unhandled React Error:', error, errorInfo);
    this.setState({ errorInfo });
  }

  reset = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
  };

  handleResetStorage = () => {
    try {
      const keysToRemove: string[] = [];
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key && key.startsWith('epi:')) {
          keysToRemove.push(key);
        }
      }
      keysToRemove.forEach((k) => localStorage.removeItem(k));
    } catch {
      /* ignore */
    }
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback(this.state.error ?? new Error('Unknown error'), this.reset);
      }
      return (
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            minHeight: '100vh',
            padding: '24px',
            backgroundColor: '#101216',
            color: '#dde1e8',
            fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
          }}
        >
          <div
            style={{
              maxWidth: '600px',
              width: '100%',
              backgroundColor: '#15181e',
              border: '1px solid #2d3340',
              borderRadius: '8px',
              padding: '28px',
              boxShadow: '0 8px 24px rgba(0,0,0,0.5)',
            }}
          >
            <h2 style={{ color: '#f87171', marginTop: 0, marginBottom: '12px', fontSize: '20px' }}>
              Something went wrong loading EPI Practice
            </h2>
            <p style={{ color: '#8e9aa8', fontSize: '14px', lineHeight: 1.5, marginBottom: '16px' }}>
              An unexpected client-side error occurred. You can reload the page or reset cached local
              state if corrupted data caused the issue.
            </p>
            {this.state.error && (
              <pre
                style={{
                  background: '#0c0e12',
                  border: '1px solid #222733',
                  padding: '12px',
                  borderRadius: '6px',
                  color: '#fca5a5',
                  fontSize: '12px',
                  overflowX: 'auto',
                  whiteSpace: 'pre-wrap',
                  wordBreak: 'break-all',
                  marginBottom: '20px',
                }}
              >
                {this.state.error.toString()}
              </pre>
            )}
            <div style={{ display: 'flex', gap: '12px' }}>
              <button
                type="button"
                onClick={() => window.location.reload()}
                style={{
                  backgroundColor: '#3b82f6',
                  color: '#ffffff',
                  border: 'none',
                  borderRadius: '6px',
                  padding: '8px 16px',
                  fontWeight: 500,
                  cursor: 'pointer',
                }}
              >
                Reload page
              </button>
              <button
                type="button"
                onClick={this.handleResetStorage}
                style={{
                  backgroundColor: '#272c36',
                  color: '#dde1e8',
                  border: '1px solid #374151',
                  borderRadius: '6px',
                  padding: '8px 16px',
                  fontWeight: 500,
                  cursor: 'pointer',
                }}
              >
                Clear saved settings & reload
              </button>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
