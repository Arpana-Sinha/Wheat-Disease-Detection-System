function Sidebar({ open, setOpen, setActivePage, logout }) {
  return (
    <div className={`sidebar ${open ? "open" : ""}`}>
      <button className="close-btn" onClick={() => setOpen(false)}>
        ✖
      </button>

      <h2>Menu</h2>

      <button
        onClick={() => {
          setActivePage("detect");
          setOpen(false);
        }}
      >
        Detect Disease
      </button>

      <button
        onClick={() => {
          setActivePage("history");
          setOpen(false);
        }}
      >
        History
      </button>

      <button
        className="logout-btn"
        onClick={() => {
          logout();
          setOpen(false);
        }}
      >
        Logout
      </button>
    </div>
  );
}

export default Sidebar;
