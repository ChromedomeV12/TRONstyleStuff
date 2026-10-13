import { Plugin } from '@opencode/plugin/tui';
import { installLogo } from './brand';

export default Plugin.define({
  id: 'tron.encomcode',
  setup(context) { return installLogo(context); },
});
