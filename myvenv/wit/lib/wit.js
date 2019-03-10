'use babel';

import WitView from './wit-view';
import { CompositeDisposable } from 'atom';

export default {

  witView: null,
  modalPanel: null,
  subscriptions: null,

  activate(state) {
    this.witView = new WitView(state.witViewState);
    this.modalPanel = atom.workspace.addModalPanel({
      item: this.witView.getElement(),
      visible: false
    });

    // Events subscribed to in atom's system can be easily cleaned up with a CompositeDisposable
    this.subscriptions = new CompositeDisposable();

    // Register command that toggles this view
    this.subscriptions.add(atom.commands.add('atom-workspace', {
      'wit:toggle': () => this.toggle()
    }));
  },

  deactivate() {
    this.modalPanel.destroy();
    this.subscriptions.dispose();
    this.witView.destroy();
  },

  serialize() {
    return {
      witViewState: this.witView.serialize()
    };
  },

  toggle() {
    console.log('Wit was toggled!');
    return (
      this.modalPanel.isVisible() ?
      this.modalPanel.hide() :
      this.modalPanel.show()
    );
  }

};
