import LeftSidebar from "./components/LeftSidebar";
import CodeEditor from "./components/CodeEditor";

export default function App() {
  return (
    <div className="h-screen w-screen flex overflow-hidden">
      <div className="flex">
        <LeftSidebar />
        <div style={{ marginLeft: 260, width: "calc(100% - 260px)" ,position:"fixed"}}>
          <CodeEditor />
        </div>
        
      </div>
    </div>
  );
}