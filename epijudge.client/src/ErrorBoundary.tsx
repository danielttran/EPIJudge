import { Component, type ReactNode } from 'react';

type Props = {
  children: ReactNode;
  fallback?: (error: Error, reset: () => void) => ReactNode;
};

type State = {
  hasError: boolean;
  error: Error | null;
};

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error) {
    console.error('Unhandled React Error:', error);
  }

  reset = () => {
    this.setState({ hasError: false, error: null });
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
            backgroundColor: 'var(--page)',
            color: 'var(--text)',
            fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
          }}
        >
          <div
            style={{
              maxWidth: '600px',
              width: '100%',
              backgroundColor: 'var(--surface)',
              border: '1px solid var(--border)',
              borderRadius: '8px',
              padding: '28px',
              boxShadow: '0 8px 24px rgba(0,0,0,0.5)',
            }}
          >
            <h2
              style={{
                color: 'var(--danger)',
                marginTop: 0,
                marginBottom: '12px',
                fontSize: '20px',
              }}
            >
              Something went wrong loading EPI Practice
            </h2>
            <p
              style={{
                color: 'var(--muted)',
                fontSize: '14px',
                lineHeight: 1.5,
                marginBottom: '16px',
              }}
            >
              An unexpected client-side error occurred. Reload the page to try again. Your saved
              answers and browser recovery copies are retained.
            </p>
            {this.state.error && (
              <pre
                style={{
                  background: 'var(--raised)',
                  border: '1px solid var(--border)',
                  padding: '12px',
                  borderRadius: '6px',
                  color: 'var(--danger)',
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
                  backgroundColor: 'var(--link)',
                  color: 'var(--surface)',
                  border: 'none',
                  borderRadius: '6px',
                  padding: '8px 16px',
                  fontWeight: 500,
                  cursor: 'pointer',
                }}
              >
                Reload page
              </button>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
