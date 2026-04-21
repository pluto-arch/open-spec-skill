;(function () {
  const useEffect = React.useEffect
  const useState = React.useState

  function StageProgress(props) {
    const entries = Object.entries(props.stageProgress || {})
    return React.createElement(
      "div",
      null,
      entries.map(function (entry) {
        const name = entry[0]
        const progress = entry[1]
        const clamped = Math.max(0, Math.min(100, progress))

        return React.createElement(
          "div",
          { className: "stage", key: name },
          React.createElement(
            "div",
            null,
            name,
            " ",
            React.createElement("span", { className: "small" }, progress + "%")
          ),
          React.createElement(
            "div",
            { className: "bar" },
            React.createElement("div", {
              className: "fill",
              style: { width: clamped + "%" }
            })
          )
        )
      })
    )
  }

  function StatusStats(props) {
    const items = Object.entries(props.statusCount || {})
    return React.createElement(
      "div",
      { className: "small" },
      items.map(function (entry) {
        return React.createElement(
          "div",
          { key: entry[0] },
          entry[0] + ": " + entry[1]
        )
      })
    )
  }

  function EventTable(props) {
    return React.createElement(
      "tbody",
      null,
      (props.events || []).map(function (ev, idx) {
        return React.createElement(
          "tr",
          { key: (ev.timestamp || "") + idx },
          React.createElement("td", null, ev.timestamp || ""),
          React.createElement("td", null, ev.feature || ""),
          React.createElement("td", null, ev.stage || ""),
          React.createElement("td", null, ev.role || ""),
          React.createElement("td", null, ev.event || ""),
          React.createElement("td", null, ev.status || ""),
          React.createElement("td", null, ev.message || "")
        )
      })
    )
  }

  function App() {
    const [summary, setSummary] = useState({
      event_count: 0,
      feature_count: 0,
      stage_progress: {},
      status_count: {},
      latest_events: []
    })

    useEffect(function () {
      let active = true

      function load() {
        fetch("/api/summary")
          .then(function (res) {
            return res.json()
          })
          .then(function (data) {
            if (active) {
              setSummary(data)
            }
          })
          .catch(function () {
            if (active) {
              setSummary(function (prev) {
                return prev
              })
            }
          })
      }

      load()
      const timer = setInterval(load, 2000)
      return function () {
        active = false
        clearInterval(timer)
      }
    }, [])

    return React.createElement(
      React.Fragment,
      null,
      React.createElement("h1", null, "Open Spec Workflow Monitor"),
      React.createElement(
        "div",
        { className: "meta" },
        "events: ",
        summary.event_count,
        " | features: ",
        summary.feature_count,
        " | updated: ",
        new Date().toLocaleTimeString()
      ),
      React.createElement(
        "div",
        { className: "grid" },
        React.createElement(
          "div",
          { className: "card" },
          React.createElement("h3", null, "阶段进度"),
          React.createElement(StageProgress, {
            stageProgress: summary.stage_progress
          })
        ),
        React.createElement(
          "div",
          { className: "card" },
          React.createElement("h3", null, "状态统计"),
          React.createElement(StatusStats, {
            statusCount: summary.status_count
          })
        )
      ),
      React.createElement(
        "div",
        { className: "card", style: { marginTop: "16px" } },
        React.createElement("h3", null, "最近事件"),
        React.createElement(
          "table",
          null,
          React.createElement(
            "thead",
            null,
            React.createElement(
              "tr",
              null,
              React.createElement("th", null, "时间"),
              React.createElement("th", null, "Feature"),
              React.createElement("th", null, "Stage"),
              React.createElement("th", null, "Role"),
              React.createElement("th", null, "Event"),
              React.createElement("th", null, "Status"),
              React.createElement("th", null, "Message")
            )
          ),
          React.createElement(EventTable, { events: summary.latest_events })
        )
      )
    )
  }

  const root = ReactDOM.createRoot(document.getElementById("root"))
  root.render(React.createElement(App))
})()
