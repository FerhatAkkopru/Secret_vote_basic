import 'reflect-metadata';
import {
  SmartContract,
  state,
  State,
  method,
  Field,
  Bool,
  Provable,
  CircuitString,
} from 'snarkyjs';

export class Voting extends SmartContract {
  @state(Field) red = State<Field>();
  @state(Field) blue = State<Field>();
  @state(Field) green = State<Field>();
  @state(Field) totalVoters = State<Field>();

  deploy(args?: any) {
    super.deploy(args);
    this.red.set(Field(0));
    this.blue.set(Field(0));
    this.green.set(Field(0));
    this.totalVoters.set(Field(0));
  }

  @method vote(
    choice: Field,
    personHash: Field,    // Kişi verilerinin hash'i
    ageProof: Field,      // Yaş kontrolü proof'u
    personProof: Field,   // Kişi doğrulama proof'u
    voteProof: Field      // Çifte oy engelleme proof'u
  ) {
    const red = this.red.get();
    const blue = this.blue.get();
    const green = this.green.get();
    const totalVoters = this.totalVoters.get();

    // State'leri okuyup bağlıyorum
    this.red.assertEquals(red);
    this.blue.assertEquals(blue);
    this.green.assertEquals(green);
    this.totalVoters.assertEquals(totalVoters);

    // Yaş kontrolü yapıyorum
    const isValidAgeProof = ageProof.equals(Field(1));
    Provable.if(isValidAgeProof, Bool(true), Bool(false)).assertTrue('Yaş 18\'den küçük olamaz');

    // Kişi verileri kontrolü yapıyorum
    const isValidPersonProof = personProof.equals(Field(1));
    Provable.if(isValidPersonProof, Bool(true), Bool(false)).assertTrue('Geçersiz kişi verileri');

    // Çifte oy kontrolü yapıyorum
    const isValidVoteProof = voteProof.equals(Field(1));
    Provable.if(isValidVoteProof, Bool(true), Bool(false)).assertTrue('Bu TC kimlik numarası daha önce oy vermiş');

    // Seçim kontrolü yapıyorum
    const isValidChoice = choice.greaterThanOrEqual(Field(0)).and(choice.lessThanOrEqual(Field(2)));
    Provable.if(isValidChoice, Bool(true), Bool(false)).assertTrue('Geçersiz seçim');

    // Hangi seçenek seçildiğini belirliyorum
    const isRed = choice.equals(Field(0));
    const isBlue = choice.equals(Field(1));
    const isGreen = choice.equals(Field(2));

    // Sayıları güncelliyorum
    const nextRed = red.add(isRed.toField());
    const nextBlue = blue.add(isBlue.toField());
    const nextGreen = green.add(isGreen.toField());
    const nextTotalVoters = totalVoters.add(Field(1));

    this.red.set(nextRed);
    this.blue.set(nextBlue);
    this.green.set(nextGreen);
    this.totalVoters.set(nextTotalVoters);

    // Kimlik bilgileri gizli kalıyor, sadece proof'lar ve seçim açık
  }
}
