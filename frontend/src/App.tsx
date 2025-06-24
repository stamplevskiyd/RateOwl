import {Routes, Route, Navigate} from 'react-router-dom';
import Navbar from '@/components/Navbar';
import Home from '@/pages/Home';
import Login from '@/pages/Login';
import {AuthProvider, useAuth} from '@/context/AuthContext';
import CreateReview from '@/pages/CreateReview';
import ReviewDetails from '@/pages/ReviewDetails';

function ProtectedRoute({children}: { children: JSX.Element }) {
    const {token} = useAuth();
    if (!token) {
        return <Navigate to="/login" replace/>;
    }
    return children;
}

export default function App() {
    return (
        <AuthProvider>
            <Navbar/>
            <div className="container mx-auto mt-4">
                <Routes>
                    <Route
                        path="/"
                        element={
                            <ProtectedRoute>
                                <Home/>
                            </ProtectedRoute>
                        }
                    />
                    <Route path="/login" element={<Login/>}/>
                    <Route path="/create" element={<CreateReview/>}/>
                    <Route path="/reviews/:id" element={<ReviewDetails />} />
                </Routes>
            </div>
        </AuthProvider>
    );
}
