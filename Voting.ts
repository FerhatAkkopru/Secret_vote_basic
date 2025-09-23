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
    nameHash: Field,      // İsim hash'i (gizli)
    surnameHash: Field,   // Soyisim hash'i (gizli)
    ageHash: Field,       // Yaş hash'i (gizli)
    ageProof: Field       // Yaş >= 18 kanıtı (gizli)
  ) {
    const red = this.red.get();
    const blue = this.blue.get();
    const green = this.green.get();
    const totalVoters = this.totalVoters.get();

    // State'i okuyup bağla
    this.red.assertEquals(red);
    this.blue.assertEquals(blue);
    this.green.assertEquals(green);
    this.totalVoters.assertEquals(totalVoters);

    // Yaş kontrolü - sadece 18+ olduğunu kanıtla
    const isValidAgeProof = ageProof.equals(Field(1));
    Provable.if(isValidAgeProof, Bool(true), Bool(false)).assertTrue('Yaş 18\'den küçük olamaz');

    // Seçim 0, 1 veya 2 olmalı
    const isValidChoice = choice.greaterThanOrEqual(Field(0)).and(choice.lessThanOrEqual(Field(2)));
    Provable.if(isValidChoice, Bool(true), Bool(false)).assertTrue('Geçersiz seçim');

    // Hangi seçenek seçildi?
    const isRed = choice.equals(Field(0));
    const isBlue = choice.equals(Field(1));
    const isGreen = choice.equals(Field(2));

    // Sayıları artır
    const nextRed = red.add(isRed.toField());
    const nextBlue = blue.add(isBlue.toField());
    const nextGreen = green.add(isGreen.toField());
    const nextTotalVoters = totalVoters.add(Field(1));

    this.red.set(nextRed);
    this.blue.set(nextBlue);
    this.green.set(nextGreen);
    this.totalVoters.set(nextTotalVoters);

    // Kimlik bilgileri gizli kalır, sadece yaş kanıtı ve seçim açık
  }
}
