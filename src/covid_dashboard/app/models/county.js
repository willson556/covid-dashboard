import Model, { attr, belongsTo } from '@ember-data/model';

export default class CountyModel extends Model {
    @attr name;
    @attr population;
    @belongsTo('state') state;
}
