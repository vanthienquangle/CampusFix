const categories = ['plumber', 'electrician', 'maintenance', 'emergency'];

export default function ReportBoard({ reports, onFinish }) {
  return (
    <div className="container">
      <h1>CampusFix Admin Dashboard</h1>
      <div className="grid">
        {categories.map((cat) => (
          <div key={cat}>
            <h3>{cat.charAt(0).toUpperCase() + cat.slice(1)}</h3>
            <ul>
              {reports.filter(r => r.category === cat).map(report => (
                <li key={report.id} style={{ textDecoration: report.finished ? 'line-through' : 'none' }}>
                  <span>{report.description} ({report.location})</span>
                  <button
                    className="btn-sm"
                    onClick={() => onFinish(report.id)}
                    disabled={report.finished}
                  >
                    Finish
                  </button>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}
