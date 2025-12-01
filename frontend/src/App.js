import LeftSidebar from "./components/LeftSidebar";
import CodeEditor from "./components/CodeEditor";

export default function App() {
  return (
    <div className="flex justify-center items-center w-screen h-screen bg-gray-900">
      {/* Fixed size box */}
      <div className="w-[900px] h-[550px] bg-white shadow-2xl rounded-xl overflow-hidden flex">
        <LeftSidebar />
        <CodeEditor />            {/* ← No extra div, no padding here */}
      </div>
    </div>
  );
}