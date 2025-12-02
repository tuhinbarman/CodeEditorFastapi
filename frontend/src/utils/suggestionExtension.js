import { Decoration, EditorView, WidgetType } from "@codemirror/view";
import { StateField } from "@codemirror/state";

class SuggestionWidget extends WidgetType {
  constructor(text) {
    super();
    this.text = text;
  }
  toDOM() {
    const span = document.createElement("span");
    span.textContent = this.text;
    span.style.opacity = "0.4";
    span.style.pointerEvents = "none";
    span.style.color = "#9CA3AF"; // Tailwind grey-400
    span.style.fontStyle = "italic";
    return span;
  }
}

function suggestionExtension(suggestion) {
  return StateField.define({
    create() {
      return Decoration.none;
    },
    update(deco, tr) {
      // Remove suggestion if document changed
      if (tr.docChanged) return Decoration.none;

      // If no suggestion, clear decorations
      if (!suggestion) return Decoration.none;

      const cursor = tr.state.selection.main.head;

      const decoBuilder = [];
      decoBuilder.push(
        Decoration.widget({
          widget: new SuggestionWidget(suggestion),
          side: 1,
        }).range(cursor)
      );

      return Decoration.set(decoBuilder);
    },
    provide: f => EditorView.decorations.from(f)
  });
}

export default suggestionExtension
